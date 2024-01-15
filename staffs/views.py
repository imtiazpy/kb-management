from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from .models import Staff, Attendance
from .forms import SaveProfileForm, AttendanceForm

class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """Visit profile page"""
        staff = get_object_or_404(Staff, user=self.request.user.id)
        mode = request.GET.get('mode', '')

        today_attendance = Attendance.objects.filter(user=request.user, date__date=date.today()).exists()
        
        context = {'staff': staff, 'today_attendance': today_attendance}


        if mode == 'edit':
            return render(request, 'staffs/profile_update.html', {'staff': staff})
        
        return render(request, 'staffs/profile_page.html', context)

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
    


class AttendanceCreateView(LoginRequiredMixin, View):
    template_name = 'staffs/attendance_page.html'
    form_name = AttendanceForm

    def get(self, request):
        user = self.request.user
        return render(request, self.template_name, {'user': user})
    
    def post(self, request):
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance created successfully.')
            return redirect('profile')
        else:
            user = self.request.user
            return render(request, self.template_name, {'user': user})


