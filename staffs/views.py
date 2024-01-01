from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Staff
from .forms import SaveProfileForm

class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """Visit profile page"""
        staff = get_object_or_404(Staff, user=self.request.user.id)
        mode = request.GET.get('mode', '')
        if mode == 'edit':
            return render(request, 'staffs/profile_update.html', {'staff': staff})
        
        return render(request, 'staffs/profile_page.html', {'staff': staff})

    def post(self, request):
        """
        Update profile (Both User and Staff Model fields)
        """
        res = {'status': 'failed', 'msg': ''}

        if not request.method == 'POST':
            res['msg'] = "No data send on this request"
        else:
            form = SaveProfileForm(request.POST, request.FILES, instance=self.request.user)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Profile has been updated")
                res['status'] = 'success'
            else:
                # Handle the error or provide feedback
                res['msg'] = 'Invalid form data'

        return JsonResponse(res)

