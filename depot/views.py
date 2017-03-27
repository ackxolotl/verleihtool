from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Depot, Item, Organization


def index(request):
    """
    Show an index page of all organizations and their depots

    Only organization managers get a link to the admin interface of their
    organization so that they can change the name and add new depots.

    :author: Florian Stamer
    :author: Benedikt Seidl
    """

    organization_depots = []

    for organization in Organization.objects.all():
        managed_by_user = organization.managed_by(request.user)
        if managed_by_user:
            depots = organization.depot_set.all()
        else:
            depots = organization.active_depots.all()

        if depots:
            organization_depots.append({
                'model': organization,
                'managed_by_user': managed_by_user,
                'depots': depots
            })

    return render(request, 'depot/index.html', {
        'organization_depots': organization_depots
    })


def detail(request, depot_id):
    """
    Provide a detailed overview of all items in a depot

    Archived depots can only be accessed by superusers and organization managers.
    The private items of a depot can be seen by all members of this organization.

    :author: Florian Stamer
    """

    depot = get_object_or_404(Depot, pk=depot_id)

    if not depot.organization.managed_by(request.user) and not depot.active:
        return HttpResponseForbidden()

    show_visibility = (request.user.is_superuser or
                       depot.organization.is_member(request.user))

    if show_visibility:
        item_list = depot.item_set.all()
    else:
        item_list = depot.public_items.all()

    error_message = None
    if 'message' in request.session:
        error_message = request.session['message']
        request.session.__delitem__('message')

    return render(request, 'depot/detail.html', {
        'depot': depot,
        'show_visibility': show_visibility,
        'managed_by_user': depot.managed_by(request.user),
        'item_list': item_list,
        'error_message': error_message,
    })
