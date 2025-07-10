from django.shortcuts import render, redirect, get_object_or_404
from .models import PlannerTask, Habit, Spending, Budget
from .forms import SpendingForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Product, CartItem
from django.contrib import messages
import json


def home(request):
    return render(request, 'main/home.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

@login_required
def planner(request):
    if request.method == 'POST':
        if 'task_id' in request.POST:
            task_obj = PlannerTask.objects.get(id=request.POST['task_id'])
            task_obj.task = request.POST['task']
            task_obj.date = request.POST['date']
            task_obj.save()
        else:
            task = request.POST.get('task')
            date_val = request.POST.get('date')
            PlannerTask.objects.create(task=task, date=date_val, user=request.user)
        return redirect('planner')

    tasks = PlannerTask.objects.filter(user=request.user).order_by('date')
    return render(request, 'main/planner.html', {'tasks': tasks})

@login_required
def delete_task(request, task_id):
    PlannerTask.objects.get(id=task_id).delete()
    return redirect('planner')

@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(PlannerTask, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('planner')

@login_required
def habits(request):
    if request.method == 'POST':
        name = request.POST['name']
        frequency = request.POST['frequency']
        start_date_val = request.POST.get('start_date', date.today())
        Habit.objects.create(name=name, frequency=frequency, start_date=start_date_val, user=request.user)
        return redirect('habits')

    habits = Habit.objects.filter(user=request.user)
    return render(request, 'main/habits.html', {'habits': habits})

@login_required
def delete_habit(request, habit_id):
    Habit.objects.get(id=habit_id).delete()
    return redirect('habits')

from django.db.models import Sum
import json

@login_required
def spending_dashboard(request):
    if request.method == 'POST':
        if 'item_name' in request.POST:  # Add spending
            form = SpendingForm(request.POST)
            if form.is_valid():
                spending = form.save(commit=False)
                spending.user = request.user
                spending.save()
                return redirect('spending_dashboard')
        elif 'category' in request.POST and 'amount' in request.POST:  # Add budget
            category = request.POST.get('category')
            amount = request.POST.get('amount')
            if category and amount:
                Budget.objects.update_or_create(
                    user=request.user,
                    category=category,
                    defaults={'amount': amount}
                )
                return redirect('spending_dashboard')

    form = SpendingForm()
    spendings = Spending.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    # Get unique categories from both spending and budget
    categories = sorted(set(
        list(spendings.values_list('category', flat=True)) +
        list(budgets.values_list('category', flat=True))
    ))

    spending_data = []
    budget_data = []

    for category in categories:
        spent = spendings.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        budget = budgets.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        spending_data.append(float(spent))
        budget_data.append(float(budget))

    context = {
        'spending_form': form,
        'spendings': spendings,
        'budgets': budgets,
        'chart_labels': json.dumps(categories),
        'spending_data': json.dumps(spending_data),
        'budget_data': json.dumps(budget_data),
    }

    return render(request, 'main/spending_dashboard.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Habit, Spending, PlannerTask
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required

@login_required
def smart_suggestions(request):
    user = request.user
    query = request.GET.get('query', '')

    # User's habit categories
    habit_categories = list(Habit.objects.filter(user=user).values_list('name', flat=True).distinct())

    # Recent categories spent on (last 30 days)
    recent_categories = list(
        Spending.objects.filter(user=user, date__gte=date.today()-timedelta(days=30))
        .values_list('category', flat=True)
        .distinct()
    )

    # Gap detector (habit but no recent spending)
    gap_categories = [cat for cat in habit_categories if cat not in recent_categories]

    # Preferred categories = habits + recent
    preferred_categories = list(set(habit_categories + recent_categories))

    if query:
        suggestions = Product.objects.filter(name__icontains=query)
    else:
        suggestions = Product.objects.filter(category__in=preferred_categories)[:24]

    return render(request, 'main/smart_suggestions.html', {
        'suggestions': suggestions,
        'gap_categories': gap_categories,
        'preferred_categories': preferred_categories,
        'query': query
    })

@login_required
def add_to_planner(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    PlannerTask.objects.create(
        user=request.user,
        task=f"Buy: {product.name}",
        date=date.today()
    )
    return redirect('smart_suggestions')
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    if request.method == 'POST':
        # simulate payment
        cart_items.delete()  # Clear cart
        messages.success(request, "Payment successful! Order placed.")
        return redirect('view_cart')

    return render(request, 'main/checkout.html', {'total': total})
