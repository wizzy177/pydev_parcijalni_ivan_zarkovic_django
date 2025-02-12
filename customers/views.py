from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Customer
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def customer_list(request):
    """
    View to list all customers.
    Supports HTML and JSON responses.
    """
    customers = Customer.objects.all()

    # JSON response
    if request.headers.get('Content-Type') == 'application/json':
        customers_data = [
            {
                "id": customer.id,
                "name": customer.name,
                "vat_id": customer.vat_id,
                "street": customer.street,
                "city": customer.city,
                "country": customer.country,
            }
            for customer in customers
        ]
        return JsonResponse(customers_data, safe=False)

    # HTML response
    return render(request,
                 'customers/customer_list.html',
                 {'customers': customers})


@login_required
@require_http_methods(["GET"])
def customer_detail(request, pk):
    """
    View to display details of a single customer.
    Supports HTML and JSON responses.
    """
    customer = get_object_or_404(Customer, pk=pk)


    # JSON response
    if request.headers.get('Content-Type') == 'application/json':
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "vat_id": customer.vat_id,
            "street": customer.street,
            "city": customer.city,
            "country": customer.country,
        }
        return JsonResponse(customer_data)

    # HTML response
    return render(request, 'customers/customer_detail.html', {'customer': customer})


@login_required
@require_http_methods(["GET", "POST"])
def customer_create(request):
    """
    View to create a new customer.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        vat_id = request.POST.get('vat_id')
        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')

        customer = Customer.objects.create(name=name, vat_id=vat_id, street=street, city=city, country=country)
    

        return redirect('customer_list')

    # Render the create form template
    return render(request,
                 'customers/customer_create_form.html',
                 {})


@login_required
@require_http_methods(["GET", "POST"])
def customer_edit(request, pk):
    """
    View to edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        # Update customer details
        customer.name = request.POST.get('name')
        customer.vat_id = request.POST.get('vat_id')
        customer.street = request.POST.get('street')
        customer.city = request.POST.get('city')
        customer.country = request.POST.get('country')
        customer.save()

        return redirect('customer_detail', pk=customer.id)

    # Render the edit form template
    return render(
        request,
        'customers/customer_edit_form.html',
        {
            'customer': customer,
        },
    )