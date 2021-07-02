from django.shortcuts import render

def contactsendemail(request):
    # new logic!
    if request.method == 'GET':
        form = contactformemail
    else:
        form = contactformemail(request.POST)
        if form.is_valid():
            frommail = form.cleaned_data['frommail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, frommail,['anjalirgupta15@gmail.com'])
    return render(request, 'Home.html', {'form': form})