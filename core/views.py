from django.shortcuts import render, redirect, get_object_or_404
from .utils import find_matches, create_notification, send_notification_email
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import LostItemForm, FoundItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Notification, LostItem, FoundItem
import re
from django.contrib.auth import get_user_model

@login_required
def report_lost(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user
            lost_item.save()
            return redirect('lost_list')
    else:
        form = LostItemForm()

    return render(request, 'core/report_lost.html', {'form': form})

@login_required
def report_found(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user
            found_item.save()

            matches = find_matches(found_item)
            if matches:
                for lost in matches:
                    # In-app notification
                    create_notification(
                        user=request.user,
                        message=f"Your found item matches Lost Item: {lost.title} (Reward: {lost.reward})",
                        link=f"/lost/{lost.id}/"
                    )
                    create_notification(
                        user=lost.user,
                        message=f"Someone reported a found item that matches your lost {lost.title}.",
                        link=f"/found/{found_item.id}/"
                    )

                    # Email to finder
                    send_notification_email(
                        request.user.email,
                        "Match Found for Your Found Item",
                        f"Your found item may match with '{lost.title}'(Reward: {lost.reward}). Check details here: http://127.0.0.1:8000/lost/{lost.id}/"
                    )

                    # Email to loser
                    send_notification_email(
                        lost.user.email,
                        "Match Found for Your Lost Item",
                        f"Someone reported a found item that may match your lost '{lost.title}'. Check details here: http://127.0.0.1:8000/found/{found_item.id}/"
                    )

            return redirect('found_list')
    else:
        form = FoundItemForm()
    return render(request, 'core/report_found.html', {'form': form})


def lost_list(request):
    from .models import LostItem
    items = LostItem.objects.all().order_by('-created_at')
    return render(request, 'core/lost_list.html', {'items': items})


def found_list(request):
    from .models import FoundItem
    items = FoundItem.objects.all().order_by('-created_at')
    return render(request, 'core/found_list.html', {'items': items})

@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notes})

@require_POST
@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications')

@require_POST
@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    messages.success(request, "All notifications cleared.")
    return redirect('notifications')

@require_POST
@login_required
def mark_read(request, note_id):
    note = get_object_or_404(Notification, id=note_id, user=request.user)
    if not note.is_read:
        note.is_read = True
        note.save(update_fields=["is_read"])
    return redirect('notifications')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    my_lost  = LostItem.objects.filter(user=request.user).order_by('-created_at')
    my_found = FoundItem.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "core/profile.html", {
        "my_lost": my_lost,
        "my_found": my_found,
    })

@require_POST
@login_required
def delete_lost_item(request, item_id):
    item = get_object_or_404(LostItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Lost item deleted.")
    return redirect("profile")

@require_POST
@login_required
def delete_found_item(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Found item deleted.")
    return redirect("profile")

def _wa_phone(phone: str) -> str:
    """Return digits-only string for WhatsApp wa.me links."""
    return re.sub(r"\D", "", phone or "")

def lost_detail(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    phone_raw = item.phone or ""
    ctx = {
        "kind": "lost",
        "item": item,
        "phone": phone_raw,           # for tel:
        "wa_phone": _wa_phone(phone_raw),  # for wa.me
        "report_url": "report_found", # opposite action
        "opposite_label": "Report Found",
        "detail_title": "LOST ITEM",
    }
    return render(request, "core/item_detail.html", ctx)

def found_detail(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id)
    phone_raw = item.phone or ""
    ctx = {
        "kind": "found",
        "item": item,
        "phone": phone_raw,           # for tel:
        "wa_phone": _wa_phone(phone_raw),  # for wa.me
        "report_url": "report_lost",  # opposite action
        "opposite_label": "I Lost This",
        "detail_title": "FOUND ITEM",
    }
    return render(request, "core/item_detail.html", ctx)

@login_required
def create_lost_item(request):
    pass

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "core/admin_dashboard.html", {"users": users})

def home(request):
    return render(request, 'core/home.html')

def base(request):
    return render(request, 'core/base.html')