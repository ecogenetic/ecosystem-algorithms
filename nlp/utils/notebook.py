import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import param
import pandas as pd
import panel as pn
import numpy

from prediction.apis import data_management_engine

def get_radio_graph(data, spoke_labels, title, sub_title):
	color = "b"
	
	N = len(data)
	
	theta = radar_factory(N, frame='polygon')

	fig, ax = plt.subplots(figsize=(4, 4), nrows=1, ncols=1,
							subplot_kw=dict(projection='radar'))
	fig.subplots_adjust(wspace=0.35, hspace=0.30, top=0.85, bottom=0.05)


	ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
	ax.set_title(sub_title, weight='bold', size='medium', position=(0.5, 1.1),
				 horizontalalignment='center', verticalalignment='center')

	ax.plot(theta, data, color=color)
	ax.fill(theta, data, facecolor=color, alpha=0.25)
	ax.set_varlabels(spoke_labels)

#	 # add legend relative to top-left plot
#	 labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
#	 legend = axs[0, 0].legend(labels, loc=(0.9, .95),
#							   labelspacing=0.1, fontsize='small')

	fig.text(0.5, 0.965, title,
			 horizontalalignment='center', color='black', weight='bold',
			 size='large')
	
	fig.patch.set_alpha(0.0)

	return fig


def radar_factory(num_vars, frame='circle'):
	"""
	Create a radar chart with `num_vars` axes.

	This function creates a RadarAxes projection and registers it.

	Parameters
	----------
	num_vars : int
		Number of variables for radar chart.
	frame : {'circle', 'polygon'}
		Shape of frame surrounding axes.

	"""
	# calculate evenly-spaced axis angles
	theta = numpy.linspace(0, 2*numpy.pi, num_vars, endpoint=False)

	class RadarAxes(PolarAxes):

		name = 'radar'
		# use 1 line segment to connect specified points
		RESOLUTION = 1

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			# rotate plot such that the first axis is at the top
			self.set_theta_zero_location('N')

		def fill(self, *args, closed=True, **kwargs):
			"""Override fill so that line is closed by default"""
			return super().fill(closed=closed, *args, **kwargs)

		def plot(self, *args, **kwargs):
			"""Override plot so that line is closed by default"""
			lines = super().plot(*args, **kwargs)
			for line in lines:
				self._close_line(line)

		def _close_line(self, line):
			x, y = line.get_data()
			# FIXME: markers at x[0], y[0] get doubled-up
			if x[0] != x[-1]:
				x = numpy.append(x, x[0])
				y = numpy.append(y, y[0])
				line.set_data(x, y)

		def set_varlabels(self, labels):
			self.set_thetagrids(numpy.degrees(theta), labels)

		def _gen_axes_patch(self):
			# The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
			# in axes coordinates.
			if frame == 'circle':
				return Circle((0.5, 0.5), 0.5)
			elif frame == 'polygon':
				return RegularPolygon((0.5, 0.5), num_vars,
									  radius=.5, edgecolor="k")
			else:
				raise ValueError("Unknown value for 'frame': %s" % frame)

		def _gen_axes_spines(self):
			if frame == 'circle':
				return super()._gen_axes_spines()
			elif frame == 'polygon':
				# spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
				spine = Spine(axes=self,
							  spine_type='circle',
							  path=Path.unit_regular_polygon(num_vars))
				# unit_regular_polygon gives a polygon of radius 1 centered at
				# (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
				# 0.5) in axes coordinates.
				spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
									+ self.transAxes)
				return {'polar': spine}
			else:
				raise ValueError("Unknown value for 'frame': %s" % frame)

	register_projection(RadarAxes)
	return theta

def generate_dashboard(auth, table_name, collection_name, key_value):
	# 45666009
	field = '{"$or":[{"employee_number":98638320}]}'
	limit = 1000
	projections = "{}"
	skip = 0

	data = data_management_engine.get_data(auth, table_name, collection_name, field, limit, projections, skip)
	df = pd.DataFrame(data)
	
	input_database = "nlp_examples"
	input_collection = "call_data_words"
	field = '{"$or":[{"callid":45666009}]}'
	# field = '{"$or":[{"employee_number":98638320}]}'
	limit = 1000
	# projections = "{}"
	projections = "channel,callid,phrase,start_time,end_time"
	skip = 0

	data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
	df_wds = pd.DataFrame(data)

	choices = list(df[key_value])
	choices.sort()
	class Dashboard(param.Parameterized):
		callid = param.Selector(default=choices[0], objects=choices)
		def tab_output(self, output, tab_depth=430):
			return pn.Row(
				pn.Column(
					width=20
				),
				pn.Column(
					output,
					width=tab_depth
				)
			)
		def get_agent_text(self):
			df_cid = df.loc[df[key_value] == self.callid]
			value = df_cid.iloc[0]["agent"]
			return self.tab_output(value, tab_depth=400)

		def get_caller_text(self):
			df_cid = df.loc[df[key_value] == self.callid]
			value = df_cid.iloc[0]["caller"]
			return self.tab_output(value, tab_depth=400)

		def get_chat(self):
			groupings = []
			ss_df = df_wds.loc[df_wds[key_value] == 45666009]
			# ss_df = df_wds.loc[df_wds[key_value] == self.callid]
			ss_df = ss_df.sort_values(by=["start_time"])
			print(ss_df)
			previous = None
			group = ""
			for index, row in ss_df.iterrows():
				phrase = row["phrase"]
				channel = row["channel"]
				st = row["start_time"]
				et = row["end_time"]
				if previous != None and channel != previous:
					dct = {
						"call_id": self.callid,
						"channel": previous,
						"text": group
					}
					groupings.append(dct)
					group = ""
				group = group + phrase + " "
				previous = channel

			chat = []
			for group in groupings:
				if group["channel"] == "left":
					row = pn.Row(
						pn.Column(
							group["text"],
							width=205
						),
						pn.Column(
							width=205
						)
					)
					chat.append(row)
				else:
					row = pn.Row(
						pn.Column(
							width=205
						),
						pn.Column(
							group["text"],
							width=205
						)
					)
					chat.append(row)
			print("HERE")
			print(chat)
			print("NOW")
			return pn.Column(*chat)

		def get_summary(self, input_database, input_collection):
			#Summary
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			asum_df = pd.DataFrame(data)
			asum_df = asum_df.loc[asum_df[key_value] == self.callid]
			return asum_df.iloc[0]["summary"]

		def get_summary_agent(self):
			value = self.get_summary(table_name, collection_name + "_agent_sum")
			return self.tab_output(value)

		def get_summary_caller(self):
			value = self.get_summary(table_name, collection_name + "_caller_sum")
			return self.tab_output(value)

		def get_b5(self, input_database, input_collection):
			#Personality B5
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			ab5_df = pd.DataFrame(data)
			ab5_df = ab5_df.loc[ab5_df[key_value] == self.callid]

			b5_list = ["conscientiousness","extraversion","stability","openess","agreeableness"]
			for b5_entry in b5_list:
				if ab5_df.iloc[0][b5_entry] == 1:
					return b5_entry
		def get_b5_agent(self):
			value = self.get_b5(table_name, collection_name + "_agent_b5")
			return self.tab_output(value)

		def get_b5_caller(self):
			value = self.get_b5(table_name, collection_name + "_caller_b5")
			return self.tab_output(value)

		def get_mbti(self, input_database, input_collection):
			#Personality MBTI
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			ambti_df = pd.DataFrame(data)
			ambti_df = ambti_df.loc[ambti_df[key_value] == self.callid]

			mbti_list = ["ISTJ","INTP","ESTJ","ISTP","ENTP","ESTP","INFJ","ISFJ","INFP","ENFJ","ESFJ","ENFP","ISFP","ESFP","INTJ","ENTJ"] 
			for mbti_entry in mbti_list:
				if ambti_df.iloc[0][mbti_entry] == 1:
					return(mbti_entry)

		def get_mbti_agent(self):
			value = self.get_mbti(table_name, collection_name + "_agent_mbti")
			return self.tab_output(value)

		def get_mbti_caller(self):
			value = self.get_mbti(table_name, collection_name + "_caller_mbti")
			return self.tab_output(value)

		#Personality POS
		def get_pos(self, input_database, input_collection):
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			apos_df = pd.DataFrame(data)
			apos_df = apos_df.loc[apos_df[key_value] == self.callid]
			return apos_df

		def get_pos_agent(self):
			return self.get_pos(table_name, collection_name + "_agent_pos")

		def get_pos_caller(self):
			return self.get_pos(table_name, collection_name + "_caller_pos")

		def get_pos_agent_verbs(self):
			pos_df = self.get_pos(table_name, collection_name + "_agent_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "VERB"]
			return self.tab_output(list(verb_df["token"]))

		def get_pos_caller_verbs(self):
			pos_df = self.get_pos(table_name, collection_name + "_caller_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "VERB"]
			return self.tab_output(list(verb_df["token"]))

		def get_pos_agent_proper_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_agent_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "PROPN"]
			verbs = list(verb_df["token"])
			verbs = ner_fix(verbs)
			return self.tab_output(verbs)

		def get_pos_caller_proper_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_caller_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "PROPN"]
			verbs = list(verb_df["token"])
			verbs = ner_fix(verbs)
			return self.tab_output(verbs)

		def get_pos_agent_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_agent_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "NOUN"]
			return self.tab_output(list(verb_df["token"]))

		def get_pos_caller_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_caller_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "NOUN"]
			return self.tab_output(list(verb_df["token"]))

		def get_pos_graph(self, input_database, input_collection):
			apos_df = self.get_pos(input_database, input_collection)
			num_records = len(apos_df.index)
			val_list = ["ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","SCONJ","VERB","X"]
			num_list = []
			if num_records == 0:
				for val in val_list:
					num_list.append(0)
			else:
				for val in val_list:
					new_df = apos_df.loc[apos_df["feature"] == val]
					count = len(new_df.index)
					num_list.append(float(count) / float(num_records))

			return get_radio_graph(num_list, val_list, "Parts of Speech" , "Distribution")

		def get_pos_graph_agent(self):
			value = self.get_pos_graph(table_name, collection_name + "_agent_pos")
			return self.tab_output(value)

		def get_pos_graph_caller(self):
			value = self.get_pos_graph(table_name, collection_name + "_caller_pos")
			return self.tab_output(value)
	return Dashboard()

def generate_dashboard_demo(auth, table_name, collection_name, key_value):
	field = ""
	limit = 0
	projections = "{}"
	skip = 0

	data = data_management_engine.get_data(auth, table_name, collection_name, field, limit, projections, skip)
	df = pd.DataFrame(data)

	choices = list(df[key_value])
	choices.sort()
	class Dashboard(param.Parameterized):
		callid = param.Selector(default=choices[0], objects=choices)
		def tab_output(self, output, tab_depth=880):
			return pn.Row(
				pn.Column(
					width=20
				),
				pn.Column(
					output,
					width=tab_depth
				)
			)
		def get_agent_text(self):
			df_cid = df.loc[df[key_value] == self.callid]
			value = df_cid.iloc[0]["text"]
			return self.tab_output(value, tab_depth=800)

		def get_summary(self, input_database, input_collection):
			#Summary
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			asum_df = pd.DataFrame(data)
			asum_df = asum_df.loc[asum_df[key_value] == self.callid]
			return asum_df.iloc[0]["summary"]

		def get_summary_agent(self):
			value = self.get_summary(table_name, collection_name + "_summarize")
			return self.tab_output(value)


		def get_b5(self, input_database, input_collection):
			#Personality B5
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			ab5_df = pd.DataFrame(data)
			ab5_df = ab5_df.loc[ab5_df[key_value] == self.callid]

			b5_list = ["conscientiousness","extraversion","stability","openess","agreeableness"]
			for b5_entry in b5_list:
				if ab5_df.iloc[0][b5_entry] == 1:
					return b5_entry
		def get_b5_agent(self):
			value = self.get_b5(table_name, collection_name + "_b5")
			return self.tab_output(value)


		def get_mbti(self, input_database, input_collection):
			#Personality MBTI
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			ambti_df = pd.DataFrame(data)
			ambti_df = ambti_df.loc[ambti_df[key_value] == self.callid]

			mbti_list = ["ISTJ","INTP","ESTJ","ISTP","ENTP","ESTP","INFJ","ISFJ","INFP","ENFJ","ESFJ","ENFP","ISFP","ESFP","INTJ","ENTJ"] 
			for mbti_entry in mbti_list:
				if ambti_df.iloc[0][mbti_entry] == 1:
					return(mbti_entry)

		def get_mbti_agent(self):
			value = self.get_mbti(table_name, collection_name + "_mbti")
			return self.tab_output(value)


		#Personality POS
		def get_pos(self, input_database, input_collection):
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip) 
			apos_df = pd.DataFrame(data)
			apos_df = apos_df.loc[apos_df[key_value] == self.callid]
			return apos_df

		def get_pos_agent(self):
			return self.get_pos(table_name, collection_name + "_pos")

		def get_pos_agent_verbs(self):
			pos_df = self.get_pos(table_name, collection_name + "_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "VERB"]
			return self.tab_output(list(verb_df["token"]))

		def get_pos_agent_proper_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "PROPN"]
			verbs = list(verb_df["token"])
			verbs = ner_fix(verbs)
			return self.tab_output(verbs)

		def get_pos_agent_nouns(self):
			pos_df = self.get_pos(table_name, collection_name + "_pos")
			verb_df = pos_df.loc[pos_df["feature"] == "NOUN"]
			return self.tab_output(list(verb_df["token"]))

		def get_ner(self, input_database, input_collection):
			field = "{}"
			limit = 0
			projections = "{}"
			skip = 0

			data = data_management_engine.get_data(auth, input_database, input_collection, field, limit, projections, skip)
			apos_df = pd.DataFrame(data)
			apos_df = apos_df.loc[apos_df[key_value] == self.callid]
			return apos_df

		def get_ner_agent(self):
			ner_df = self.get_ner(table_name, collection_name + "_ner")
			new_list = []
			words = list(ner_df["word"])
			entities = list(ner_df["entity"])
			for i in range(len(words)):
				new_list.append(words[i] + ": " + entities[i])
			return self.tab_output(new_list)

		def get_pos_graph(self, input_database, input_collection):
			apos_df = self.get_pos(input_database, input_collection)
			num_records = len(apos_df.index)
			val_list = ["ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","SCONJ","VERB","X"]
			num_list = []
			if num_records == 0:
				for val in val_list:
					num_list.append(0)
			else:
				for val in val_list:
					new_df = apos_df.loc[apos_df["feature"] == val]
					count = len(new_df.index)
					num_list.append(float(count) / float(num_records))

			return get_radio_graph(num_list, val_list, "Parts of Speech" , "Distribution")

		def get_pos_graph_agent(self):
			value = self.get_pos_graph(table_name, collection_name + "_pos")
			return self.tab_output(value)

	return Dashboard()


def ner_fix(nouns):
	if len(nouns) == 0:
		return []
	new_nouns = [nouns[0]]
	for i in range(1,len(nouns)):
		word = nouns[i]
		if word[:2] == "##":
			new_nouns[-1] = new_nouns[-1] + word[2:]
		else:
			new_nouns.append(word)
	return new_nouns