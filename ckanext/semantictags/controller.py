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

	def load_global_tags(self):
		import urllib2
		import urllib
		import json

		global_tags_response = False

		try:			
			global_tags_response = urllib2.urlopen('http://stodap.org/tags/Special:Ask/-5B-5BCategory:muto:Tag-5D-5D/format%3Djson/offset%3D0')
		except:
			1 == 1
	
		if global_tags_response: 
			gtag_list_dict = json.loads(global_tags_response.read())	
			gtag_list = gtag_list_dict["results"]
			for tag in gtag_list:
				x = db.SemanticTag(gtag_list_dict["results"][tag]["fullurl"], gtag_list_dict["results"][tag]["fullurl"])
				x.save()
				#print gtag_list_dict["results"][tag]["fulltext"] + " " + gtag_list_dict["results"][tag]["fullurl"]

		else:
			print "fails"

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

