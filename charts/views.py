from django.shortcuts import render
from allModel.models import *
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404,render_to_response,RequestContext 
from django.template import RequestContext,loader
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
import MLP,PIL,PIL.Image,StringIO,matplotlib.pyplot as plt,numpy as np
from django.core.context_processors import request
from reportlab.pdfgen.canvas import Canvas
from matplotlib import pylab
from gnome import canvas
from MySQLdb.constants.FIELD_TYPE import NULL
from chartit import DataPool, Chart
import random,datetime,time

# Create your views here.
def allcharts(request):
    print "Learning the sin function"
    network =MLP.MLP(2,10,1)
   
    samples = np.zeros(2000, dtype=[('x',  float, 1), ('y', float, 1)])
    samples['x'] = np.linspace(-5,5,2000)
    samples['y'] = np.sin(samples['x'])
    #samples['y'] = np.linspace(-4,4,2500)

    for i in range(100000):
        n = np.random.randint(samples.size)
        network.propagate_forward(samples['x'][n])
        network.propagate_backward(samples['y'][n])

    plt.figure(figsize=(10,5))
    # Draw real function

    x = samples['x']
    y = samples['y'] 
    #x=np.linspace(-6.0,7.0,50)
    plt.plot(x,y,color='b',lw=1)


    samples1 = np.zeros(2000, dtype=[('x1',  float, 1), ('y1', float, 1)])
    samples1['x1'] = np.linspace(-4,4,2000)
    samples1['y1'] = np.sin(samples1['x1'])

    # Draw network approximated function
    for i in range(samples1.size):
        samples1['y1'][i] = network.propagate_forward(samples1['x1'][i])
        #x[i] = network.propagate_backward(y[i])

    #pl.plot(samples['x'], samples['y'] ,'.',x , y, '-')
    #l.legend(['train target', 'net output'])
    #pl.show()
    plt.plot(samples1['x1'],samples1['y1'],color='r',lw=3)
    plt.axis([-2,2,-2,2])
    plt.show()
    plt.close()
    return HttpResponseRedirect('/charts/charts')  
    #buffer=StringIO.StringIO()
    #canvas=pylab.get_current_fig_manager().canvas
    #canvas.draw()
    #graphIMG =PIL.Image.fromstring("RGB",canvas.get_width_height(),canvas.tostring_rgb())
    #graphIMG.save(buffer, "PNG")
    #pylab.close()
    #return HttpResponse(buffer.getvalue(),content_type="image/png")
    #return render(request, 'pages/forms/charts.html',context_instance=RequestContext(request))  
    
def linecharts(request):
    print "Learning the line function"
    network =MLP.MLP(2,10,1)
   
    samples = np.zeros(2000, dtype=[('x',  float, 1), ('y', float, 1)])
    samples['x'] = np.linspace(-5,5,2000)
    samples['y'] = np.linspace(-5,5,2000)
    #samples['y'] = np.linspace(-4,4,2500)

    for i in range(100000):
        n = np.random.randint(samples.size)
        network.propagate_forward(samples['x'][n])
        network.propagate_backward(samples['y'][n])

    plt.figure(figsize=(10,5))
    # Draw real function

    x = samples['x']
    y = samples['y'] 
    #x=np.linspace(-6.0,7.0,50)
    plt.plot(x,y,color='b',lw=1)


    samples1 = np.zeros(1000, dtype=[('x1',  float, 1), ('y1', float, 1)])
    samples1['x1'] = np.linspace(-8,8,1000)
    samples1['y1'] = np.linspace(-8,8,1000)

    # Draw network approximated function
    for i in range(samples1.size):
        samples1['y1'][i] = network.propagate_forward(samples1['x1'][i])
        #x[i] = network.propagate_backward(y[i])

    #pl.plot(samples['x'], samples['y'] ,'.',x , y, '-')
    #l.legend(['train target', 'net output'])
    #pl.show()
    plt.plot(samples1['x1'],samples1['y1'],color='r',lw=3)
    plt.axis([-1,1,-1,1])
    plt.show()
    plt.close()
    return HttpResponseRedirect('/charts/charts')  


def paraboliccharts(request):
    print "Learning the parabolic function"
    network = MLP.MLP(1,10,1)
    samples = np.zeros(500, dtype=[('x',  float, 1), ('y', float, 1)])
    samples['x'] = np.linspace(0,1,500)
    samples['y'] = np.sin(samples['x']*np.pi)

    for i in range(10000):
        n = np.random.randint(samples.size)
        network.propagate_forward(samples['x'][n])
        network.propagate_backward(samples['y'][n])

    plt.figure(figsize=(10,5))
    # Draw real function
    x,y = samples['x'],samples['y']
    plt.plot(x,y,color='b',lw=1)
    # Draw network approximated function
    for i in range(samples.shape[0]):
        y[i] = network.propagate_forward(x[i])
    plt.plot(x,y,color='r',lw=3)
    plt.axis([0,1,0,1])
    plt.show()
    plt.close()
    return HttpResponseRedirect('/charts/charts')  


def charts(request):
    try:
        request.session['user_login_data']
        dept_data=SuUserDepartment.objects.filter(org=request.session['user_login_data']['org'])
        
        
       
        """
        pieChart
        """
        
        #--- creating piechart Survey Answred vs Unanswresd ----
        
        allsurveyassign=SuSureyAndUser.objects.count()
        answered=SuSureyAndUser.objects.filter(is_answered=1).count()
        unanswred=SuSureyAndUser.objects.exclude(is_answered__isnull=False).count()
        
        xdata_Answred_vs_Unanswresd = ["Answered", "Unanswered"]
        ydata_Answred_vs_Unanswresd = [answered, unanswred]
    
        color_list_Answred_vs_Unanswresd = ['#1df021', '#e32636']
        extra_serie_Answred_vs_Unanswresd = {
            "tooltip": {"y_start": "", "y_end": " emplyees"},
            "color_list": color_list_Answred_vs_Unanswresd
        }
        chartdata_Answred_vs_Unanswresd = {'x': xdata_Answred_vs_Unanswresd, 'y1': ydata_Answred_vs_Unanswresd, 'extra1': extra_serie_Answred_vs_Unanswresd}
        charttype_Answred_vs_Unanswresd = "pieChart"
        chartcontainer_Answred_vs_Unanswresd = 'piechart_container'  # container name
        
        #--- creating piechart Survey Answred vs Unanswresd ----
        
        #--- creating piechart active users vs inactive users ----
        
        active=SuUser.objects.filter(is_active=1).count()
        inactive=SuUser.objects.exclude(is_active=1).count()
        totalemp=SuUser.objects.count()
        
        xdata_active_vs_inactive = ["active", "inactive"]
        ydata_active_vs_inactive = [active, inactive]
    
        color_list_active_vs_inactive = ['#1df021', '#e32636']
        extra_serie_active_vs_inactive = {
            "tooltip": {"y_start": "", "y_end": " emplyees"},
            "color_list": color_list_active_vs_inactive
        }
        chartdata_active_vs_inactive = {'x': xdata_active_vs_inactive, 'y1': ydata_active_vs_inactive, 'extra1': extra_serie_active_vs_inactive}
        charttype_active_vs_inactive = "pieChart"
        chartcontainer_active_vs_inactive = 'piechart_container_active_vs_inactive'  # container name
        
        #--- creating piechart active users vs inactive users ----
        
        
        """
        barchart 
        """
        
        #--- creating barchart Employee vs subfactor ----
               
        numberEmployees=SuSubFactorAvarage.objects.values_list('sum',flat=True).order_by('sum')
        subfactor=SuSubFactorAvarage.objects.select_related().values_list('subfactor',flat=True).order_by('sum')
        subfactorsName=[]
        mainfactorName=[]
        
        for sub in subfactor:
            mainfactorName.append(SuSubFactors.objects.get(id=sub).main_factor.factor)
            subfactorsName.append(SuSubFactors.objects.get(id=sub).factor)
        
        xdata_employee_vs_subfactor = subfactorsName
        ydata_employee_vs_subfactor = numberEmployees
    
       
        extra_serie_employee_vs_subfactor = {
            "tooltip": {"y_start": "", "y_end": " employees"},
            
        }
        chartdata_employee_vs_subfactor = {'x': xdata_employee_vs_subfactor, 'y1': ydata_employee_vs_subfactor, 'extra1': extra_serie_employee_vs_subfactor}
        charttype_employee_vs_subfactor = "discreteBarChart"
        chartcontainer_employee_vs_subfactor = 'discreteBarChart_Employee_vs_subfactor'  # container name
        
        
        #--- creating barchart Employee vs subfactor ----
        
        
        #--- creating barchart Employee vs mainfactor ----
        
        xdata_employee_vs_mainfactor = mainfactorName
        ydata_employee_vs_mainfactor = numberEmployees
    
        
        extra_serie_employee_vs_mainfactor = {
            "tooltip": {"y_start": "", "y_end": " employees"},
            
        }
        chartdata_employee_vs_mainfactor = {'x': xdata_employee_vs_mainfactor, 'y1': ydata_employee_vs_mainfactor, 'extra1': extra_serie_employee_vs_mainfactor}
        charttype_employee_vs_mainfactor = "discreteBarChart"
        chartcontainer_employee_vs_mainfactor = 'discreteBarChart_Employee_vs_mainfactor'  # container name
        
        #--- creating barchart Employee vs mainfactor ----
        
        
        #--- creating barchart Employee vs Surey ----
        
        countSurey=[]
        sureyName=[]
        
        countSurey_Surey=SuSureyAndUser.objects.values('surey').annotate(dcount=Count('surey')).filter(is_answered=1)
        
        for both in countSurey_Surey:
            sureyName.append(SuSurey.objects.get(id=both['surey']).su_name)
            countSurey.append(both['dcount'])
       
        xdata_employeeCount_vs_Surey = sureyName
        ydata_employeeCount_vs_Surey = countSurey
    
        
        extra_serie_employeeCount_vs_Surey = {
            "tooltip": {"y_start": "", "y_end": " Employee Answers"},
            
        }
        chartdata_employeeCount_vs_Surey = {'x': xdata_employeeCount_vs_Surey, 'y1': ydata_employeeCount_vs_Surey, 'extra1': extra_serie_employeeCount_vs_Surey}
        charttype_employeeCount_vs_Surey = "discreteBarChart"
        chartcontainer_employeeCount_vs_Surey = 'discreteBarChart_employeeCount_vs_Surey'  # container name
          
        #--- creating barchart EmployeeCount vs Surey ----
        
        
        data = {
                
            ##### Answred_vs_Unanswresd #####
            'charttype_Answred_vs_Unanswresd': charttype_Answred_vs_Unanswresd,
            'chartdata_Answred_vs_Unanswresd': chartdata_Answred_vs_Unanswresd,
            'chartcontainer_Answred_vs_Unanswresd': chartcontainer_Answred_vs_Unanswresd,
            ##### Answred_vs_Unanswresd #####
            
            
            ##### active_vs_inactive #####
            'charttype_active_vs_inactive': charttype_active_vs_inactive,
            'chartdata_active_vs_inactive': chartdata_active_vs_inactive,
            'chartcontainer_active_vs_inactive': chartcontainer_active_vs_inactive,
            ##### active_vs_inactive #####
            
            
            ##### employee_vs_subfactor #####
            'charttype_employee_vs_subfactor': charttype_employee_vs_subfactor,
            'chartdata_employee_vs_subfactor': chartdata_employee_vs_subfactor,
            'chartcontainer_employee_vs_subfactor': chartcontainer_employee_vs_subfactor,
            ##### employee_vs_subfactor #####
            
             ##### employee_vs_mainfactor #####
            'charttype_employee_vs_mainfactor': charttype_employee_vs_mainfactor,
            'chartdata_employee_vs_mainfactor': chartdata_employee_vs_mainfactor,
            'chartcontainer_employee_vs_mainfactor': chartcontainer_employee_vs_mainfactor,
            ##### employee_vs_subfactor #####
            
            ##### employee Count_vs_Surey #####
            'charttype_employeeCount_vs_Surey': charttype_employeeCount_vs_Surey,
            'chartdata_employeeCount_vs_Surey': chartdata_employeeCount_vs_Surey,
            'chartcontainer_employeeCount_vs_Surey': chartcontainer_employeeCount_vs_Surey,
            ##### employee Count_vs_Surey #####
            
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },
                
            'dept_data': dept_data,'allsurveyassign':allsurveyassign,'totalemp':totalemp,
        } 
        
        
        return render(request, 'pages/forms/charts.html',data,context_instance=RequestContext(request))   
        
    
    except KeyError, e:
        messages={'alert':'No activity within 120 minutes; please log in again'}
        return render(request, 'index.html',{'messages': messages},context_instance=RequestContext(request))   
     
def demo_multibarchart(request):
    """
    multibarchart page
    """
    nb_element = 10
    xdata = range(nb_element)
    ydata = [random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)
    ydata3 = map(lambda x: x * 3, ydata)
    ydata4 = map(lambda x: x * 4, ydata)

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
        'name3': 'series 3', 'y3': ydata3, 'extra3': extra_serie,
        'name4': 'series 4', 'y4': ydata4, 'extra4': extra_serie
    }

    nb_element = 100
    start_time = int(time.mktime(datetime.datetime(2012, 2, 1).timetuple()) * 1000)
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                   "date_format": tooltip_date}

    date_chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarChart"
    chartcontainer = 'multibarchart_container'  # container name
    chartcontainer_with_date = 'date_multibarchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'chartdata_with_date': date_chartdata,
        'chartcontainer_with_date1': chartcontainer_with_date,
        'extra_with_date': {
            'name': chartcontainer_with_date,
            'x_is_date': True,
            'x_axis_format': '%d %b %Y',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
    }
    return render_to_response('multibarchart.html', data)     

def demo_discretebarchart_with_date(request):
    try:
        request.session['user_login_data']
        dept_data=SuUserDepartment.objects.filter(org=request.session['user_login_data']['org'])
        allsurveyassign=SuSureyAndUser.objects.count()
        answered=SuSureyAndUser.objects.filter(is_answered=1).count()
        unanswred=SuSureyAndUser.objects.exclude(is_answered__isnull=False).count()
        
        """
        discretebarchart page
        """
        start_time = int(time.mktime(datetime.datetime(2014, 6, 1).timetuple()) * 1000)
        nb_element = 10
        ss=time.mktime(datetime.datetime(2014, 6, 1).timetuple()) * 1000 
        xdata = list(range(nb_element))
        xdata = [start_time + x * 1000000000 for x in xdata]
        ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    
        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {
            'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'  # container name
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': True,
                'x_axis_format': '%d-%b',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },
        }
            
        return render(request, 'pages/forms/discretebarchart_with_date.html',data,context_instance=RequestContext(request))   
            
        
    except KeyError, e:
        messages={'alert':'No activity within 120 minutes; please log in again'}
        return render(request, 'index.html',{'messages': messages},context_instance=RequestContext(request))
        
def test_charts(request):
    try:
        request.session['user_login_data']
        dept_data=SuUserDepartment.objects.filter(org=request.session['user_login_data']['org'])
        allsurveyassign=SuSureyAndUser.objects.count()
        answered=SuSureyAndUser.objects.filter(is_answered=1).count()
        unanswred=SuSureyAndUser.objects.exclude(is_answered__isnull=False).count()
        
         #Step 1: Create a DataPool with the data we want to retrieve.
        weatherdata = \
            DataPool(
               series=
                [{'options': {
                   'source': ChartdemoMonthlyweatherbycity.objects.all()},
                  'terms': [
                    'month',
                    'houston_temp',]}
                 ])
    
        #Step 2: Create the Chart object
        cht = Chart(
                datasource = weatherdata,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                      'month': [
                        'houston_temp']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Weather Data of Boston and Houston'},
                   'xAxis': {
                        'title': {
                           'text': 'Month number'}}})
    
        #Step 3: Send the chart object to the template.
        return render(request,'pages/tet.html',{'weatherchart': cht},context_instance=RequestContext(request))
        #return render(request, 'pages/forms/charts.html',{'dept_data': dept_data,'allsurveyassign':allsurveyassign,'answered':answered,'unanswred':unanswred},context_instance=RequestContext(request))   
        
    
    except KeyError, e:
        messages={'alert':'No activity within 120 minutes; please log in again'}
        return render(request, 'index.html',{'messages': messages},context_instance=RequestContext(request)) 
    
def CurrentEmp(request):
    try:
        request.session['user_login_data']
        pass
    except KeyError, e:
        messages={'alert':'No activity within 120 minutes; please log in again'}
        return render(request, 'index.html',{'messages': messages},context_instance=RequestContext(request)) 
    