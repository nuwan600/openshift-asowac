from django.shortcuts import render
from allModel.models import *
from gnome import canvas
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404,render_to_response,RequestContext 

# Create your views here.
def test(request):
    try:
        request.session['user_login_data']
        dept_data=SuUserDepartment.objects.filter(org=request.session['user_login_data']['org'])
        allsurveyassign=SuSureyAndUser.objects.count()
        answered=SuSureyAndUser.objects.filter(is_answered=1).count()
        unanswred=SuSureyAndUser.objects.exclude(is_answered__isnull=False).count()
        
        #--- creating piechart ----
        """
        pieChart page
        """
        xdata = ["Answered", "Unanswered"]
        ydata = [answered, unanswred]
    
        color_list = ['#1df021', '#e32636']
        extra_serie = {
            "tooltip": {"y_start": "", "y_end": " emplyees"},
            "color_list": color_list
        }
        chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
        charttype = "pieChart"
        chartcontainer = 'piechart_container'  # container name
    
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        } 
        
        
        
        userAndSurey=SuSureyAndUser.objects.get(surey=SuSurey.objects.get(id=45),user=SuUser.objects.get(id=6))
       
        
        
        return render(request, 'pages/forms/test.html',data,context_instance=RequestContext(request))   
        
    
    except KeyError, e:
        messages={'alert':'No activity within 120 minutes; please log in again'}
        return render(request, 'index.html',{'messages': messages},context_instance=RequestContext(request)) 
     