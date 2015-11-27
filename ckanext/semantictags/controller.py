import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

import ckan.plugins as p
from ckan.lib.base import BaseController, response, request
import json
import db
import ckan.model as model
import plugin

c = p.toolkit.c
render = p.toolkit.render

class SemantictagsController(BaseController):

    #index function for display form to load datasets for managing their relations
	def index(self):
		return render('semantictags/index.html')

	def show_semantictags(self):
		return render('semantictags/semantictags.html')

	def show_tag_semantictags(self):
		return render('semantictags/tag_semantictags.html')

	def show_suggestions(self):
		return render('semantictags/suggestions.html')

	def show_predicates(self):
		return render('semantictags/predicates.html')

	def associate(self):
		x = db.TagSemanticTag(model.tag.Tag.by_id(request.POST['tag_id']), db.SemanticTag.by_URI(request.POST['URI']))
		#x.semantictag = db.SemanticTag.by_URI(request.POST['URI'])
		#x.tag = model.tag.Tag.by_id(request.POST['tag_id'])
		x.save()
		return render('semantictags/tag_semantictags.html')

	def add_semantictag(self):
		x = db.SemanticTag(request.POST['URI'], request.POST['label'])
		x.save()
		return render('semantictags/semantictags.html')

	def add_predicate(self):
		x = db.Predicate(request.POST['namespace'], request.POST['prefix'], request.POST['predicate'])
		x.save()
		return render('semantictags/predicates.html')


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
				x = db.SemanticTag(gtag_list_dict["results"][tag]["fullurl"], gtag_list_dict["results"][tag]["fulltext"])
				x.save()
				#print gtag_list_dict["results"][tag]["fulltext"] + " " + gtag_list_dict["results"][tag]["fullurl"]

		else:
			print "fails"

		return render('semantictags/semantictags.html')

	def associate_equal_tags(self):
		suggestions = plugin.suggest_tag_semantictag()
		for sug in suggestions:
			x = db.TagSemanticTag(model.tag.Tag.by_id(sug[1]['id']), sug[0])	
			x.save()
		return render('semantictags/tag_semantictags.html')

	def remove_semantictag(self):
		x = db.SemanticTag.get(request.GET['id'])
		import ckan.model.meta as meta
		meta.Session.delete(x)
		meta.Session.commit()

		return render('semantictags/semantictags.html')

	def remove_all_semantictag(self):
		all_ = db.SemanticTag.list_all()
		for x in all_:
			x.delete()
			x.commit()
		return render('semantictags/semantictags.html')

	def remove_predicate(self):
		x = db.Predicate.by_id(request.GET['id'])
		x.delete()
		x.commit()
		return render('semantictags/predicates.html')

	def remove_all_predicates(self):
		all_ = db.Predicate.list_all()
		for x in all_:
			x.delete()
			x.commit()
		return render('semantictags/predicates.html')

	def remove_tag_semantictag(self):
		x = db.TagSemanticTag.get(request.GET['id'])
		x.delete()
		x.commit()
		return render('semantictags/tag_semantictags.html')

	def remove_all_tag_semantictag(self):
		all_ = db.TagSemanticTag.list_all()
		for x in all_:
			x.delete()
			x.commit()
		return render('semantictags/tag_semantictags.html')

