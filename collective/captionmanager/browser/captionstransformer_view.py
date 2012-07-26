#python
from captionstransformer import registry
from StringIO import StringIO

#zope
from zope import interface
from zope import component
from zope import schema
from z3c.form import form, button

#plone
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.field import NamedFile
from plone.z3cform import layout

from collective.captionmanager.i18n import captionmanagerMessageFactory as _
from collective.captionmanager import vocabulary

class FormSchema(interface.Interface):
    """Schema for this form"""

    input_file = schema.Bytes(title=_(u"input file"),
                           required=False)

    input_text = schema.Text(title=_(u"input text"),
                             required=False)

    input_format = schema.Choice(title=_(u"input format"),
                                 description=_(u"input_format_description"),
                                 vocabulary=vocabulary.format_vocabulary,
                                 required=False)

    output_format = schema.Choice(title=_(u"output format"),
                                 description=_(u"output_format_description"),
                                 vocabulary=vocabulary.format_vocabulary)


class Form(AutoExtensibleForm, form.Form):
    schema = FormSchema
    label = _(u"Captions transformer form")

    @button.buttonAndHandler(_(u'Transform'))
    def handle_transform(self, action):
        data, errors = self.extractData()
        input_info = registry.REGISTRY.get(data['input_format'])
        output_info = registry.REGISTRY.get(data['output_format'])
        filename = 'captions%s' % output_info['extension']

        text = None
        if data['input_text'] and not data['input_file']:
            text = StringIO(data['input_text'])
        elif data['input_file']:
            text = StringIO(data['input_file'])

        if text is None:
            raise Exception # TODO manage errors

        reader = input_info['reader'](text)
        captions = reader.read()

        writer = output_info['writer'](StringIO())
        writer.set_captions(captions)
        output = writer.captions_to_text()

        response = self.request.response
        contenttype = "%s; charset=utf-8" % output_info['mimetype']
        response.setHeader("Content-type", contenttype)

        response.setHeader("Content-disposition",
                           "attachment;filename=%s"%filename)
        response.write(output.encode('utf-8'))
        return output


class FormAdapter(object):
    interface.implements(FormSchema)
    def __init__(self, context):
        self.context = context


class CaptionsTransformerView(layout.FormWrapper):
    form = Form
