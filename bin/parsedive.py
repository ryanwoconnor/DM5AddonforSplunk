import xml.etree.ElementTree as ET
import os
import time
import datetime

directory='../sample/'

for file in os.listdir(directory):
    if file.endswith(".sml"):
    	filetime = os.path.getmtime(directory+file)
    	now = time.time()
    	five_minutes_ago = now-3600
    	if filetime > five_minutes_ago:
			tree = ET.parse(os.path.join(directory, file))
			root = tree.getroot()
		
			date_time = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Header/{http://www.suunto.com/schemas/sml}DateTime')
			duration = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Header/{http://www.suunto.com/schemas/sml}Duration')
			max_depth = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Header/{http://www.suunto.com/schemas/sml}Depth/{http://www.suunto.com/schemas/sml}Max')
			serial_number = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Device/{http://www.suunto.com/schemas/sml}SerialNumber')
			software_version = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Device/{http://www.suunto.com/schemas/sml}Info/{http://www.suunto.com/schemas/sml}SW')
			device_name = root.find('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Device/{http://www.suunto.com/schemas/sml}Name')
		
			pattern = '%Y-%m-%dT%H:%M:%S'
			epoch = int(time.mktime(time.strptime(date_time.text, pattern)))
		
			print str(epoch)+' event=dive_summary duration='+duration.text+ ' max_depth='+max_depth.text+' software_version='+software_version.text+' serial_number='+serial_number.text+ ' device_name='+device_name.text

			i = -1
			for samples in root.findall('./{http://www.suunto.com/schemas/sml}DeviceLog/{http://www.suunto.com/schemas/sml}Samples'):
				for sample in samples:
					if i == -1:
						i = i + 1
						continue
					i = i + 1
					event_sample=''
					time = sample.find('{http://www.suunto.com/schemas/sml}Time')
					depth = sample.find('{http://www.suunto.com/schemas/sml}Depth')
					temp = sample.find('{http://www.suunto.com/schemas/sml}Temperature')
					if time is not None:
						event_sample=event_sample+str(int(time.text)+epoch)
					if depth is not None:
						event_sample=event_sample+' depth='+depth.text
					if temp is not None:
						event_sample=event_sample+' temp='+ temp.text
					events = sample.findall('{http://www.suunto.com/schemas/sml}Events/{http://www.suunto.com/schemas/sml}State')
					for event in events:
						type = event.find('{http://www.suunto.com/schemas/sml}Type')
						active = event.find('{http://www.suunto.com/schemas/sml}Active')
						if type is not None and active is not None:
							if type.text=='Below Surface' and active.text=='false':
								event_sample=event_sample+' depth=0'
							else:
								continue
					if 'depth' in event_sample:
						print event_sample