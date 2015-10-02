import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

import ckan.plugins as p
from ckan.lib.base import BaseController, response, request
import json
import db
import ckan.model as model

c = p.toolkit.c
render = p.toolkit.render

class SemantictagsController(BaseController):

    #index function for display form to load datasets for managing their relations
    def index(self):
        return render('semantictags/index.html')

    def associate(self):
	x = db.TagSemanticTag(model.tag.Tag.by_id(request.POST['tag_id']), db.SemanticTag.by_URI(request.POST['URI']))
	#x.semantictag = db.SemanticTag.by_URI(request.POST['URI'])
	#x.tag = model.tag.Tag.by_id(request.POST['tag_id'])
	x.save()
        return render('semantictags/index.html')

    def add_semantictag(self):
	x = db.SemanticTag(request.POST['URI'], request.POST['label'])
	x.save()
        return render('semantictags/index.html')

#    def delete(self):
#        p.toolkit.get_action('tag_delete')({},{'id': request.POST['tag']})
#        return render('tagmanager/index.html')

#    def merge(self):
#        "assign all elements tagged with tag2 with tag1; delete tag2"

#        tag2_datasets = p.toolkit.get_action('tag_show')({},{'id' : request.POST['tag2'], 'include_datasets': True})

#        for ds in tag2_datasets['packages']:
#            dataset = p.toolkit.get_action('package_show')({},{'id': ds['id'] })
#            dataset['tags'].append(p.toolkit.get_action('tag_show')({},{'id':request.POST['tag1']}))
#            p.toolkit.get_action('package_update')({},dataset)

#        p.toolkit.get_action('tag_delete')({},{'id': request.POST['tag2']})

#        #p.toolkit.redirect_to(controller='tagmanager', action='index')

#        return render('tagmanager/index.html')

