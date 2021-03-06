from django.views.generic import View, TemplateView
from django.http import HttpResponse, StreamingHttpResponse
from .usbcam import MJpegStreamCam
 
mjpegstream = MJpegStreamCam(IP_address="172.30.1.33")
 
class CamView(TemplateView):
    template_name = "cam.html"
 
    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode", "#")
        return context
 
# def snapshot(request):
#     image = mjpegstream.snapshot()
#     return HttpResponse(image, content_type="image/jpeg")
 
def mjpeg_stream(request):
    # mjpegstream.start()
    return StreamingHttpResponse(mjpegstream, content_type='multipart/x-mixed-replace;boundary=myboundary')
