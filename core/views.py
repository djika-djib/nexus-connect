from .models import CorePillar, Service
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from django.db import OperationalError


def home(request):
    try:
        pillars = CorePillar.objects.all()
        services = Service.objects.all()
    except OperationalError as e:
        # Log would be better to a logger; for now render a simple maintenance/fallback view
        return render(request, 'core/maintenance.html', {
            'message': 'Database not ready yet. Please check deployment logs.'
        }, status=503)

    return render(request, 'core/home.html', {'pillars': pillars, 'services': services})


# def home(request):
#     pillars = CorePillar.objects.all()
#     services = Service.objects.all()
#     return render(request, 'core/home.html', {'pillars': pillars, 'services': services})

def about(request):
    return render(request, 'core/about.html')

def services_page(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})

# def contact(request):
#     return render(request, 'core/contact.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Compose email
            full_message = f"From: {name} <{email}>\n\n{message}"

            try:
                send_mail(
                    subject=subject or f"Contact from {name}",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
                return redirect('core:contact')
            except Exception as e:
                # Log e if you have logging; show a friendly message
                messages.error(request, "Sorry — we couldn't send your message right now. Try again later.")
                return redirect('core:contact')

            messages.success(request, "Thanks — your message has been sent. We'll be in touch soon.")
            return redirect('core:contact')  # Post/Redirect/Get pattern
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
