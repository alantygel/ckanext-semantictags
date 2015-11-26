import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import db
import ckan.model as model

def list_tags():
	return plugins.toolkit.get_action('tag_list')({},{'all_fields' : True})

def list_semantictags():
	return db.SemanticTag.list_all()

def list_predicates():
	return db.Predicate.list_all()

def list_unique_predicates():
	return db.Predicate.list_unique()

def list_tag_semantictags():
	return db.TagSemanticTag.list_all()

def tag_show(id):
	return model.tag.Tag.by_id(id).name

def semantictag_show(id):
	return db.SemanticTag.by_id(id).URI

def find_tag_semantictag(tag_id): 
	res = db.TagSemanticTag.by_tag_id(tag_id)
	if res:
		return db.SemanticTag.by_id(res.semantictag_id)
	else:
		return None

def suggest_tag_semantictag(): 
	stags = list_semantictags()
	tags = list_tags()
	suggestions = []
	for st in stags:
		for t in tags:
			if st.label.lower() == t['name'].lower():
				suggestions.append([st, t])

	return suggestions

class SemantictagsPlugin(plugins.SingletonPlugin):
	plugins.implements(plugins.IConfigurer)
	# IConfigurer

	plugins.implements(plugins.IConfigurable)
	plugins.implements(plugins.IRoutes, inherit=True)
	plugins.implements(plugins.ITemplateHelpers)

	def configure(self, config):
		self.site_url = config.get('ckan.site_url')

	def before_map(self, map):
		semantictags = 'ckanext.semantictags.controller:SemantictagsController'

		map.connect('/semantictags', 'semantictags', controller=semantictags, action='index')
		map.connect('/semantictags/show_semantictags', controller=semantictags, action='show_semantictags')
		map.connect('/semantictags/show_tag_semantictags', controller=semantictags, action='show_tag_semantictags')
		map.connect('/semantictags/show_suggestions', controller=semantictags, action='show_suggestions')
		map.connect('/semantictags/show_predicates', controller=semantictags, action='show_predicates')
		map.connect('/semantictags', controller=semantictags, action='index')
		map.connect('/semantictags/associate', controller=semantictags, action='associate')
		map.connect('/semantictags/add_semantictag', controller=semantictags, action='add_semantictag')
		map.connect('/semantictags/add_predicate', controller=semantictags, action='add_predicate')
		map.connect('/semantictags/load_global_tags', controller=semantictags, action='load_global_tags')	
		map.connect('/semantictags/associate_equal_tags', controller=semantictags, action='associate_equal_tags')	
		map.connect('/semantictags/remove_semantictag', controller=semantictags, action='remove_semantictag')	
		map.connect('/semantictags/remove_all_semantictag', controller=semantictags,
 action='remove_all_semantictag')	
		map.connect('/semantictags/remove_predicate', controller=semantictags, action='remove_predicate')	
		map.connect('/semantictags/remove_all_predicates', controller=semantictags,
 action='remove_all_predicates')	
		map.connect('/semantictags/remove_tag_semantictag', controller=semantictags, action='remove_tag_semantictag')	
		map.connect('/semantictags/remove_all_tag_semantictag', controller=semantictags, action='remove_all_tag_semantictag')	

		return map

	def after_map(self, map):
		return map

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'semantictags')

	def get_helpers(self):
		return {'semantictags_list_tags':list_tags,'semantictags_tag_show':tag_show, 'semantictags_list_semantictags':list_semantictags, 'semantictags_list_tag_semantictags' : list_tag_semantictags, 'semantictags_semantictag_show': semantictag_show, 'semantictags_find_tag_semantictag' : find_tag_semantictag, 'semantictags_suggest_tag_semantictag': suggest_tag_semantictag,  'semantictags_list_predicates':list_predicates,'semantictags_list_unique_predicates':list_unique_predicates}


