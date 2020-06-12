from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class EmployeeRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.editor


class UserOrStaffMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return self.request.user == object.user or self.request.user.is_staff
