
from django.shortcuts import render, get_object_or_404, redirect
import uuid

from .qr import generate_qr
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse

from .models import Event, Category, Registration
from .forms import EventForm, RegistrationForm, SignUpForm


# --------------------------------
# EVENT LIST
# --------------------------------

def event_list(request):

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    time_filter = request.GET.get('filter', 'upcoming').strip()

    events = Event.objects.all()

    if time_filter == 'upcoming':
        events = events.filter(start_time__gte=timezone.now())

    elif time_filter == 'past':
        events = events.filter(end_time__lt=timezone.now())

    if category_slug:
        events = events.filter(category__slug=category_slug)

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    categories = Category.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': query,
        'time_filter': time_filter,
    }

    return render(request, 'events/event_list.html', context)


# --------------------------------
# EVENT DETAIL
# --------------------------------

def event_detail(request, slug):

    event = get_object_or_404(Event, slug=slug)

    user_registration = None

    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(
            user=request.user,
            event=event,
            status='CONFIRMED'
        ).first()

    form = RegistrationForm()

    context = {
        'event': event,
        'user_registration': user_registration,
        'form': form,
    }

    return render(request, 'events/event_detail.html', context)


# --------------------------------
# CREATE EVENT
# --------------------------------

@login_required
def event_create(request):

    if not hasattr(request.user, 'profile') or not request.user.profile.is_organizer:
        messages.error(request, "Only Organizer accounts are permitted to create events. Please sign up as an Organizer.")
        return redirect('event_list')

    if not Category.objects.exists():
        Category.objects.create(name="General", icon="fa-bookmark")

    if request.method == 'POST':

        form = EventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            messages.success(request, f"Event '{event.title}' created successfully!")

            return redirect('event_detail', slug=event.slug)

    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {
        'form': form,
        'title': 'Create New Event'
    })


# --------------------------------
# EDIT EVENT
# --------------------------------

@login_required
def event_edit(request, slug):

    event = get_object_or_404(Event, slug=slug)

    if event.organizer != request.user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('event_detail', slug=event.slug)

    if request.method == 'POST':

        form = EventForm(request.POST, instance=event)

        if form.is_valid():

            event = form.save()

            messages.success(request, f"Event '{event.title}' updated successfully!")

            return redirect('event_detail', slug=event.slug)

    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'title': f'Edit {event.title}',
        'event': event
    })


# --------------------------------
# DELETE EVENT
# --------------------------------

@login_required
def event_delete(request, slug):

    event = get_object_or_404(Event, slug=slug)

    if event.organizer != request.user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('event_detail', slug=event.slug)

    if request.method == 'POST':

        title = event.title
        event.delete()

        messages.success(request, f"Event '{title}' deleted successfully.")

        return redirect('dashboard')

    return render(request, 'events/event_confirm_delete.html', {
        'event': event
    })


# --------------------------------
# REGISTER EVENT
# --------------------------------

@login_required
def register_event(request, slug):

    event = get_object_or_404(Event, slug=slug)

    if event.is_past:
        messages.error(request, "Cannot register for past events.")
        return redirect('event_detail', slug=event.slug)

    tickets = int(request.POST.get('tickets_count', 1))

    if tickets < 1:
        messages.error(request, "Please select at least one ticket.")
        return redirect('event_detail', slug=event.slug)

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event,
        defaults={
            'tickets_count': tickets,
            'status': 'CONFIRMED'
        }
    )

    if not created:

        if registration.status == 'CANCELLED':

            registration.status = 'CONFIRMED'
            registration.tickets_count = tickets
            registration.ticket_id = "EVH-" + uuid.uuid4().hex[:8].upper()
            registration.is_used = False

            registration.save()

            generate_qr(registration)

            messages.success(request, f"Your registration for '{event.title}' has been re-confirmed!")

        else:

            messages.info(request, f"You are already registered for '{event.title}'.")

    else:

        registration.ticket_id = "EVH-" + uuid.uuid4().hex[:8].upper()

        registration.save()

        generate_qr(registration)

        messages.success(request, f"Successfully registered for '{event.title}' ({tickets} ticket(s))!")

    return redirect('event_detail', slug=event.slug)


# --------------------------------
# CANCEL REGISTRATION
# --------------------------------

@login_required
def cancel_registration(request, slug):

    event = get_object_or_404(Event, slug=slug)

    registration = Registration.objects.filter(
        user=request.user,
        event=event,
        status='CONFIRMED'
    ).first()

    if registration:

        registration.status = 'CANCELLED'
        registration.save()

        messages.success(request, f"Your registration for '{event.title}' has been cancelled.")

    else:

        messages.error(request, "Active registration not found.")

    return redirect('event_detail', slug=event.slug)


# --------------------------------
# USER DASHBOARD
# --------------------------------

@login_required
def dashboard(request):

    user_registrations = Registration.objects.filter(
        user=request.user,
        status='CONFIRMED'
    ).select_related('event')

    organized_events = Event.objects.filter(
        organizer=request.user
    )

    context = {
        'registrations': user_registrations,
        'organized_events': organized_events,
    }

    return render(request, 'events/dashboard.html', context)


# --------------------------------
# SIGNUP
# --------------------------------

def signup_view(request):

    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, f"Welcome to EventHub, {user.username}!")

            return redirect('event_list')

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


# --------------------------------
# ORGANIZER QR SCANNER
# --------------------------------

@login_required
def qr_scanner(request):

    if not hasattr(request.user, 'profile') or not request.user.profile.is_organizer:

        messages.error(request, "Only organizers can access the QR scanner.")

        return redirect('event_list')

    return render(request, 'events/qr_scanner.html')


# --------------------------------
# VERIFY TICKET
# --------------------------------

def _verify_response(request, message, valid, registration=None):
    """Return JSON for the scanner's fetch() call, or the HTML page for a plain form post."""

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        data = {'message': message, 'valid': valid}

        if registration:
            data.update({
                'attendee': registration.user.get_full_name() or registration.user.username,
                'event': registration.event.title,
                'tickets_count': registration.tickets_count,
                'ticket_id': registration.ticket_id,
            })

        return JsonResponse(data)

    return render(request, 'events/qr_scanner.html', {
        'message': message,
        'valid': valid,
    })


@login_required
def verify_ticket(request):

    if request.method != 'POST':
        return redirect('qr_scanner')

    ticket_id = (request.POST.get('ticket_id') or '').strip()

    registration = Registration.objects.select_related('event', 'user').filter(
        ticket_id=ticket_id,
        status='CONFIRMED'
    ).first()

    if not registration:
        return _verify_response(request, 'Invalid Ticket!', False)

    if registration.event.organizer != request.user and not request.user.is_superuser:
        return _verify_response(request, 'You are not authorized to verify this ticket.', False)

    # Atomic update so two rapid scans of the same QR can't both succeed
    updated = Registration.objects.filter(pk=registration.pk, is_used=False).update(is_used=True)

    if not updated:
        return _verify_response(request, 'Ticket Already Used!', False, registration)

    return _verify_response(request, 'Valid Ticket! Attendee Checked In.', True, registration)


# --------------------------------
# ATTENDEE CHECK-IN STATUS
# --------------------------------

@login_required
def check_ticket_status(request):

    ticket_id = request.GET.get('ticket_id')

    if not ticket_id:

        return JsonResponse({
            'error': 'Ticket ID is required'
        }, status=400)

    registration = Registration.objects.filter(
        ticket_id=ticket_id,
        user=request.user,
        status='CONFIRMED'
    ).first()

    if not registration:

        return JsonResponse({
            'error': 'Ticket not found'
        }, status=404)

    return JsonResponse({
        'ticket_id': registration.ticket_id,
        'is_used': registration.is_used,
        'status': 'Checked In' if registration.is_used else 'Not Checked In'
    })
