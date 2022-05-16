# -*- coding: utf-8 -*-

import re
import json
import htmlmin
from glob import glob

from collections import Counter

def main():
	for path in glob('../keyphrases/*.json'):
		issueID = path[path.rfind('/')+1:path.find('.json')]

		print(issueID)

		generateHTML(issueID)


def generateHTML(issueID):
	with open(f'../keyphrases/{issueID}.json', 'r') as r:
		data = json.load(r)

	meeting = data['meetingRecord'][0]

	issue_name = f'第{meeting["session"]}回国会 {meeting["nameOfHouse"]} {meeting["nameOfMeeting"]} {meeting["issue"]}'
	issue_date = meeting['date']

	kps = []
	num_speech = len(meeting['speechRecord'])
	for speech in meeting['speechRecord']:
		kps += speech['keyphrase']
	counts = Counter(kps)

	div_speeches = []
	for speech in meeting['speechRecord']:
		### Speech block with header
		div_speech = f'''
			<div class='row speech-block'>
				<div class='col-12 speaker-metadata'>
					[{speech['speechOrder']}] {speech['speaker']}（{speech['speakerPosition']}）
				</div>
				<div class='col-md-8 speech'> 
		'''

		### Speech text for highlight
		speech_txt = speech['speech']
		kp_txt = []
		for kp in sorted(speech['keyphrase'], key=lambda x: counts[x]):
			pattern = re.compile(re.escape(kp), re.IGNORECASE)
			speech_txt = pattern.sub(f'<span class="keyphrase">{kp}</span>', speech_txt)
			kp_txt.append(f'<li>{kp} ({counts[kp]})</li>')
		div_speech += speech_txt.replace('\n', '<br>') + "</div>"

		kp_txt = ''.join(kp_txt)

		### Keyphrase list
		div_speech += f'<div class="col-md-4 keyphrase-list"><ul>{kp_txt}</ul></div>'

		### Close speech block
		div_speech += '</div>'
		div_speeches.append(div_speech)

	div_speeches = ''.join(div_speeches)

	div_issue = f'''
		<link rel="stylesheet" href="/css/minute.css">
		<div class='issue-block'>
			<div class='issue-body'>
				{div_speeches}
			</div>
		</div>
	'''

	out = f'''---
title: "{issue_name}"
publishdate: {issue_date}
draft: false
---
''' + htmlmin.minify(div_issue)

	with open(f'../keyphrases/markdown/{issueID}.md', 'w') as w:
		w.write(out)


if __name__ == "__main__":
    main()
