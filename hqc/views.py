from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from hqc.models import Message, Reply
from flask.ext.mongoengine.wtf import model_form


messages =Blueprint('messages', __name__, template_folder='templates')


class ListView(MethodView):
    """ get all messages.

    """
    #exclude should add msg_id
    form = model_form(Message, exclude=[ 'created_at', 'is_show',
                                        'tags', 'replies'])

    def get_context(self):
        msgs = Message.objects.all()
        form = self.form(request.form)

        context = {
            "msgs": msgs,
            "form": form
        }
        return context

    def get(self):
        context = self.get_context()
        #messages = Message.objects.all()
        return render_template('list.djhtml', **context)

    def post(self):
        context = self.get_context()
        form = context.get('form')

        if form.validate():
            new_msg = Message()
            form.populate_obj(new_msg)

            #newmsg.msg_id = some_random_mothod_to_get_id()
            new_msg.save()
            return redirect(url_for('messages.list'))
        return render_template('list.djhtml', **context)



class DetailView(MethodView):
    """display message detail.

    """
    def get(self, msg_id):
        msg = Message.objects.get_or_404(msg_id=msg_id)
        return render_template('detail.djhtml', msg=msg)


messages.add_url_rule('/' , view_func=ListView.as_view('list'))
messages.add_url_rule('/<msg_id>/', view_func=DetailView.as_view('detail'))
