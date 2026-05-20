from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Supplier, Part, Transaction


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_parts = Part.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    low_stock_parts = Part.objects.filter(quantity__lte=5).order_by('quantity')
    low_stock_count = low_stock_parts.count()
    recent_transactions = Transaction.objects.select_related('part', 'user').order_by('-date')[:10]

    return render(request, 'dashboard.html', {
        'total_parts': total_parts,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_parts': low_stock_parts,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    })


# ─── Parts ───────────────────────────────────────────────────────────────────

@login_required
def part_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    parts = Part.objects.select_related('category', 'supplier').order_by('-created_at')

    if query:
        parts = parts.filter(Q(part_name__icontains=query) | Q(description__icontains=query))
    if category_id:
        parts = parts.filter(category__id=category_id)

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'parts/part_list.html', {
        'parts': parts,
        'categories': categories,
        'suppliers': suppliers,
        'query': query,
        'selected_category': category_id,
    })


@login_required
def part_add(request):
    if request.method == 'POST':
        part_name = request.POST.get('part_name', '').strip()
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier')
        quantity = request.POST.get('quantity', 0)
        price = request.POST.get('price', 0)
        description = request.POST.get('description', '').strip()

        if not part_name:
            messages.error(request, 'Part name is required.')
            return redirect('part-list')

        part = Part.objects.create(
            part_name=part_name,
            category_id=category_id if category_id else None,
            supplier_id=supplier_id if supplier_id else None,
            quantity=quantity,
            price=price,
            description=description,
        )

        if int(quantity) > 0:
            Transaction.objects.create(
                part=part,
                transaction_type=Transaction.IN,
                quantity=quantity,
                user=request.user,
            )

        messages.success(request, f'Part "{part_name}" added successfully.')
    return redirect('part-list')


@login_required
def part_edit(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        part_name = request.POST.get('part_name', '').strip()
        if not part_name:
            messages.error(request, 'Part name is required.')
            return redirect('part-list')
        part.part_name = part_name
        part.category_id = request.POST.get('category') or None
        part.supplier_id = request.POST.get('supplier') or None
        part.quantity = request.POST.get('quantity', 0)
        part.price = request.POST.get('price', 0)
        part.description = request.POST.get('description', '').strip()
        part.save()
        messages.success(request, f'Part "{part.part_name}" updated successfully.')
    return redirect('part-list')


@login_required
def part_delete(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        name = part.part_name
        part.delete()
        messages.success(request, f'Part "{name}" deleted.')
    return redirect('part-list')


# ─── Categories ──────────────────────────────────────────────────────────────

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Category name is required.')
        else:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" added successfully.')
    return redirect('category-list')


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Category name is required.')
        else:
            category.name = name
            category.save()
            messages.success(request, f'Category "{name}" updated successfully.')
    return redirect('category-list')


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
    return redirect('category-list')


# ─── Suppliers ───────────────────────────────────────────────────────────────

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        if not name:
            messages.error(request, 'Supplier name is required.')
        else:
            Supplier.objects.create(name=name, contact=contact)
            messages.success(request, f'Supplier "{name}" added successfully.')
    return redirect('supplier-list')


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        if not name:
            messages.error(request, 'Supplier name is required.')
        else:
            supplier.name = name
            supplier.contact = contact
            supplier.save()
            messages.success(request, f'Supplier "{name}" updated successfully.')
    return redirect('supplier-list')


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{name}" deleted.')
    return redirect('supplier-list')


# ─── Transactions ─────────────────────────────────────────────────────────────

@login_required
def transaction_list(request):
    transactions = Transaction.objects.select_related('part', 'user').order_by('-date')
    parts = Part.objects.all().order_by('part_name')
    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'parts': parts,
    })


@login_required
def transaction_add(request):
    if request.method == 'POST':
        part_id = request.POST.get('part')
        transaction_type = request.POST.get('transaction_type')
        quantity = request.POST.get('quantity', 0)

        try:
            quantity = int(quantity)
        except ValueError:
            messages.error(request, 'Invalid quantity.')
            return redirect('transaction-list')

        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than zero.')
            return redirect('transaction-list')

        part = get_object_or_404(Part, pk=part_id)

        if transaction_type == Transaction.OUT and quantity > part.quantity:
            messages.error(request, f'Not enough stock. Only {part.quantity} units available.')
            return redirect('transaction-list')

        if transaction_type == Transaction.IN:
            part.quantity += quantity
        else:
            part.quantity -= quantity
        part.save()

        Transaction.objects.create(
            part=part,
            transaction_type=transaction_type,
            quantity=quantity,
            user=request.user,
        )

        messages.success(request, 'Transaction recorded successfully.')
    return redirect('transaction-list')
