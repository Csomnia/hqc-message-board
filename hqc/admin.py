from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from hqc.auth import require_auth
from hqc.models import HqcMessage,HqcReply
from hqc.mail import send_email


admin = Blueprint('admin', __name__, template_folder='templates')

class List(MethodView):
    decorators = [require_auth]

    def get(self):
        msgs = HqcMessage.objects.all()
        return render_template('admin/list.djhtml', msgs=msgs)


class Detail(MethodView):
    decorators = [require_auth]
    reply_form = model_form(HqcReply, exclude=['created_at'])

    def get_context(self, msg_id):
        msg = HqcMessage.objects.get_or_404(msg_id=msg_id)
        form = self.reply_form(request.form)
        context = {
            "msg": msg,
            "form":form
        }
        return context


    def get(self, msg_id):
        context = self.get_context(msg_id)
        return render_template('admin/detail.djhtml', **context)

    # def send_email(self, recipient):
    #     mail = Mail(app)
    #     mail_msg = Mail_msg("",
    #                         sender=("LaoWang", "laowang@shuibiao.com"),
    #                         recipients=[recipient])
    #     mail_msg.body = "tong xue cha shui biao!"
    #     mail_html = "<h2>shun feng shui biao</h2>"
    #    mail.send(mail_msg)

    def post(self, msg_id):
        context = self.get_context(msg_id)
        form = context.get('form')
        #print(form.validate())

        if form.validate():
            new_reply = HqcReply()
            form.populate_obj(new_reply)
            edit_msg = HqcMessage.objects.get_or_404(msg_id=msg_id)
            edit_msg.replies.append(new_reply)
            edit_msg.save()
            recipent = [edit_msg.email]
            send_email("has been replied", recipent)
            return redirect(url_for('admin.detail', msg_id=msg_id))
        return render_template('admin/detail.djhtml', **context)
# class MailTest(MethodView):

#     def post(self):
#         recipient=str(request.form.get("recipient"))
#         mail = Mail(app)
#         mail_msg = Message("nihao",
#                             sender=("LaoWang", "laowang@shuibiao.com"),
#                             recipients=[recipient])
#         mail_msg.body = "tong xue cha shui biao!"
#         mail_html = "<h2>shun feng shui biao</h2>"
#         mail.send(mail_msg)
#         return str(recipient)

class MsgOperate(MethodView):
    decorators = [require_auth]

    def post(self):
        msg_id = int(request.form.get('msg_id'))
        comm = str(request.form.get('comm'))
        #print(msg_id)
        edit_msg = HqcMessage.objects.get_or_404(msg_id=msg_id)
        if comm == 'del':
            edit_msg.delete()
        elif comm == 'show':
            if edit_msg.is_show:
                edit_msg.is_show = False
            else:
                edit_msg.is_show = True
            edit_msg.save()

        return "sccuess"


admin.add_url_rule('/admin/', view_func=List.as_view('list'))
admin.add_url_rule('/admin/<msg_id>/', view_func=Detail.as_view('detail'))
admin.add_url_rule('/admin/comm/',view_func=MsgOperate.as_view('command'))
