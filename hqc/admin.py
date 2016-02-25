from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from hqc.auth import require_auth
from hqc.models import Message,Reply


admin = Blueprint('admin', __name__, template_folder='templates')

class List(MethodView):
    decorators = [require_auth]

    def get(self):
        msgs = Message.objects.all()
        return render_template('admin/list.djhtml', msgs=msgs)


class Detail(MethodView):
    docorators = [require_auth]
    reply_form = model_form(Reply, exclude=['created_at'])

    def get_context(self, msg_id):
        msg = Message.objects.get_or_404(msg_id=msg_id)
        form = self.reply_form(request.form)
        context = {
            "msg": msg,
            "form":form
        }
        return context


    def get(self, msg_id):
        context = self.get_context(msg_id)
        return render_template('admin/detail.djhtml', **context)

    def post(self, msg_id):
        context = self.get_context(msg_id)
        form = context.get('form')
        print(form.validate())

        if form.validate():
            new_reply = Reply()
            form.populate_obj(new_reply)
            edit_msg = Message.objects.get_or_404(msg_id=msg_id)
            edit_msg.replies.append(new_reply)
            edit_msg.save()
            return redirect(url_for('admin.detail', msg_id=msg_id))
        return render_template('admin/detail.djhtml', **context)


admin.add_url_rule('/admin/', view_func=List.as_view('list'))
admin.add_url_rule('/admin/<msg_id>/', view_func=Detail.as_view('detail'))
