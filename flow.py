import gtk
import gobject
import httplib
import json
entry = gtk.Entry()
fixed=gtk.Fixed()
image=gtk.Image()
ControllerFrame=gtk.Frame()
SwitchesFrame=gtk.Frame()
AddFlowFrame=gtk.Frame()
ListFlowFrame=gtk.Frame()
AddFlowFrame=gtk.Frame()
delFlowFrame=gtk.Frame()
ListDeviceFrame=gtk.Frame()

notebook = gtk.Notebook()
notebook.set_tab_pos(gtk.POS_TOP)
controller=gtk.Label("Controller :")
ListFlow=gtk.Label("List Flow :")
AddFlow=gtk.Label("Add Flow :")
delFlow=gtk.Label("Delete Flow :")
switches=gtk.Label("Switches : ")
ListDevice=gtk.Label("Hosts :")


addSwitch=gtk.Label("switch: ")
addName=gtk.Label("name: ")

'''addCookie=gtk.Label("cookie: ")'''
addActions=gtk.Label("actions: ")
addPriority=gtk.Label("priority: ")
addingressport=gtk.Label("ingress-port: ")
addActive=gtk.Label("active: ")
addOutput=gtk.Label("Output: ")


addSwitchValue = gtk.Label()
addNameValue=gtk.Label()
addCookieValue=gtk.Label()
addPriorityValue=gtk.Label()
addingressportValue=gtk.Label()
addActiveValue=gtk.Label()
addActionsValue=gtk.Label()
addOutputValue=gtk.Label()
combobox_1 = gtk.ComboBox()
cell = gtk.CellRendererText()


liststore = gtk.ListStore(str)
Controllerfixed=gtk.Fixed()
SwitchesFixed=gtk.Fixed()
AddFlowFixed=gtk.Fixed()
ListFlowFixed=gtk.Fixed()
ListDeviceFixed=gtk.Fixed()

switchEntry=gtk.Entry()
nameEntry=gtk.Entry()
cookieEntry=gtk.Entry()
priorityEntry=gtk.Entry()
ingressportEntry=gtk.Entry()
activeEntry=gtk.Entry()
outputEntry=gtk.Entry()

DialogLabel=gtk.Label()

flowname=gtk.Label("Flow Name :")
'''ListFlowCookie=gtk.Label("Cookie")'''
'''ListFlowCookier=gtk.Label()'''

deleteFlowFixed=gtk.Fixed()
deleteFlowEntry=gtk.Entry()

flowButton=gtk.Button("Add Flow")
DelButton=gtk.Button("Enter Flow Name")

headers = {
           			 'Content-type': 'application/json',
            		 'Accept': 'application/json',
           }
conn = httplib.HTTPConnection('172.16.116.134', 8080)


ListFlowfinal=gtk.Label()
ControllerDetailsfinal=gtk.Label()
SwitchesDetailsfinal=gtk.Label()
ListDevicefinal=gtk.Label()

class childwindow(gtk.Window):
	def __init__(self):
		
		super(childwindow, self).__init__()
       		self.connect("destroy", gtk.main_quit)
		self.set_size_request(500, 500)
		self.set_position(gtk.WIN_POS_CENTER)
        	self.set_title("SDN Manager1")
	  	self.ControllerDetails()
	  	self.SwitchesDetails()
	  	self.ListFlow()
	  	self.AddFlow()
	  	self.deleteFlow()
	  	self.ListDevice()

		notebook.insert_page(ControllerFrame,controller,0)
		notebook.insert_page(SwitchesFrame,switches,1)
		notebook.insert_page(ListFlowFrame,ListFlow,2)
		notebook.insert_page(ListDeviceFrame,ListDevice,3)
		notebook.insert_page(AddFlowFrame,AddFlow,4)
		notebook.insert_page(delFlowFrame,delFlow,5)
		
		notebook.set_current_page(0)
		flowButton.connect("clicked",self.Add_Flow)
		DelButton.connect("clicked",self.delete_Flow)

		self.add(notebook)
		self.show_all()

	def ListDevice(self):
		conn.request('GET','/wm/device/')
		response=conn.getresponse()
		ret=response.read()
		deviceDetails=json.loads(ret)
		conn.close()
		listdevice1=" "
		ip=" "
		ap=" "
		for data in deviceDetails:
			
			
		
			if len(data['attachmentPoint']) > 0 :
				if len(data['ipv4']) > 0 :
					 
					listdevice1=listdevice1+"Mac Address : \t\t"+data['mac'][0]+"\n" + "IPV4 :\t\t" +data['ipv4'][0]+"\n\n"+"Port : \t\t\t"+str(data['attachmentPoint'][0]['port'])+"\n"+"Switch ID: \t\t " + data['attachmentPoint'][0]['switchDPID']  +" \n \n "
				else:
					listdevice1=listdevice1+"Mac Address : \t\t"+data['mac'][0]+"\n" + "IPV4 :\t\t" +"\n\n"+"Port : \t\t\t"+str(data['attachmentPoint'][0]['port'])+"\n\n"+"Switch ID: \t\t " + data['attachmentPoint'][0]['switchDPID']  +" \n \n "
		
		ListDevicefinal.set_markup(listdevice1)
		ListDeviceFixed.put(ListDevicefinal,50,50)
		ListDeviceFrame.add(ListDeviceFixed)
		
	def deleteFlow(self):

		deleteFlowFixed.put(DelButton,180,300)
		deleteFlowFixed.put(deleteFlowEntry,150,250)
		delFlowFrame.add(deleteFlowFixed)




	def delete_Flow(self,widget):
		delflow=json.dumps({"name":deleteFlowEntry.get_text()})
		path = '/wm/staticflowentrypusher/json'
		conn.request('DELETE',path,delflow,headers)
		response=conn.getresponse()
		ret=response.read()
		
		message=gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup(ret)
		message.run()

		notebook.remove_page(2)
		
		self.ListFlow()
		notebook.insert_page(ListFlowFrame,ListFlow,2)
		notebook.set_current_page(2)
		self.show_all()

	def ListFlow(self):
		conn.request('GET','/wm/staticflowentrypusher/list/all/json')
		response=conn.getresponse()
		ret=response.read()
		fdetails=json.loads(ret)
		conn.close()
		listflow1=" "
		
		for head in fdetails:
			
			for data in fdetails[head]:
				
				
				listflow1=listflow1+"\nSwitch ID: \t \t" + head + "\n"
				listflow1=listflow1+"Flow Name : \t \t" + data + "\n" 
				''' "Cookie : \t \t" + str(fdetails[head][data]['cookie'])+"\n"'''
				listflow1=listflow1+"Output Port : \t\t" + str(fdetails[head][data]['actions'][0]['port'])+"\n"
				listflow1=listflow1+"Input Port  : \t\t"+ str(fdetails[head][data]['match']['inputPort'])+"\n"
				listflow1=listflow1+"dataLayerDestination  : \t\t"+ str(fdetails[head][data]['match']['dataLayerDestination'])+"\n"
				listflow1=listflow1+"dataLayerSource  : \t\t"+ str(fdetails[head][data]['match']['dataLayerSource'])+" \n \n"	
				
											
		
		ListFlowfinal.set_markup(listflow1)
		ListFlowFixed.put(ListFlowfinal,50,50)
		ListFlowFrame.add(ListFlowFixed)
			
					
	def Add_Flow(self,widget):
		index=combobox_1.get_active()
		model=combobox_1.get_model()
		item=model[index]
		action=item[0]
		
		output = "" 
		if outputEntry.get_text()=="all":
			output = "all"
		else:
			output="output="+outputEntry.get_text()
		

		flow=json.dumps({
					"switch":switchEntry.get_text(),
					"name":nameEntry.get_text(),
					"cookie":"0",
					"priority":priorityEntry.get_text(),
					"ingress-port":ingressportEntry.get_text(),
					"active":activeEntry.get_text(),
					"actions":output

			})
		
		path = '/wm/staticflowentrypusher/json'
		body=json.dumps(flow)
		conn.request('POST',path,flow,headers)
		response=conn.getresponse()
		ret=response.read()
		
		message=gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup(ret)
		message.run()

		page = notebook.get_current_page()
		notebook.remove_page(2)
		
		
		self.ListFlow()
		notebook.insert_page(ListFlowFrame,ListFlow,2)
		notebook.set_current_page(2)
		self.show_all()
		
	def ControllerDetails(self):
		
		conn.request('GET','/wm/core/memory/json')
		response = conn.getresponse()
		ret = response.read()
		conn.close()
		cdetails=json.loads(ret)
		ControllerDetails1="Controller IP: \t\t\t " + entry.get_text() + "\n" + "Free Memory Available : \t\t" + str(cdetails['free']) + "\n" + "Total Memory Available : \t\t" + str(cdetails['total'])
		ControllerDetailsfinal.set_markup(ControllerDetails1)
		
		Controllerfixed.put(ControllerDetailsfinal,50,50)
		ControllerFrame.add(Controllerfixed)

	def AddFlow(self):

		AddFlowFixed.put(addSwitch,100,50)
		AddFlowFixed.put(switchEntry,200,50)
		AddFlowFixed.put(addName,100,70)
		AddFlowFixed.put(nameEntry,200,70)
		'''
		AddFlowFixed.put(addCookie,100,90)
		
		AddFlowFixed.put(cookieEntry,200,90)
		'''
		AddFlowFixed.put(addPriority,100,110)
		AddFlowFixed.put(priorityEntry,200,110)
		AddFlowFixed.put(addingressport,100,130)
		AddFlowFixed.put(ingressportEntry,200,130)
		AddFlowFixed.put(addActive,100,150)
		AddFlowFixed.put(activeEntry,200,150)
		AddFlowFixed.put(addOutput,100,170)
		AddFlowFixed.put(flowButton,140,190)

		self.createComboBox()
		AddFlowFixed.put(outputEntry,200,170)
		'''AddFlowFixed.put(combobox_1,200,170)'''
		AddFlowFrame.add(AddFlowFixed)
		


	def createComboBox(self):
        	liststore.append(['Select:'])
      		liststore.append(['All'])
        	liststore.append(['controller'])
        	liststore.append(['local'])
        	liststore.append(['ingress-port'])
        	liststore.append(['normal'])
        	liststore.append(['flood'])
     		
        combobox_1.pack_start(cell)
        combobox_1.add_attribute(cell, 'text', 0)
        combobox_1.set_model(liststore)
        combobox_1.set_active(0)

	def SwitchesDetails(self):

	        conn.request('GET','/wm/core/switch/all/desc/json')
       		response=conn.getresponse()
        	ret=response.read()
        	sdetails=json.loads(ret)
        	row=50
        	column=100
        	conn.close()
        	switchdetails1=" "
        	

        	for head in sdetails:
        		switchdetails1=switchdetails1+"Switch ID :\t\t\t\t" + head + "\n" 
    
        		for data in sdetails[head]:

 					switchdetails1=switchdetails1+"Software Description: \t\t" + data['softwareDescription']+ "\n" + "Data Path Description : \t\t" + data['datapathDescription']+ "\n" 	
 					switchdetails1=switchdetails1 + "Hardware Description: \t\t" + data['hardwareDescription'] + "\n" + "Manufacturer Description : \t" + data['manufacturerDescription'] + "\n"
 			
 			
 			SwitchesDetailsfinal.set_markup(switchdetails1)
 			SwitchesFixed.put(SwitchesDetailsfinal,50,50)
        	SwitchesFrame.add(SwitchesFixed)
        			
        			

        			
class sdnmanager(gtk.Window):
	def on_clicked(self,widget):
                childwindow()
		self.window.destroy()
	
	def __init__(self):
		super(sdnmanager, self).__init__()
		self.connect("destroy", gtk.main_quit)
		self.set_size_request(500, 500)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title("SDN Manager")
		
		btn1=gtk.Button("Enter IP Address")
		fixed.put(entry,150,250)
		image.set_from_file("floodlight.jpg")
		fixed.put(btn1, 180, 300)
		fixed.put(image,100,100)
		btn1.set_tooltip_text("Ex : 172.16.116.134")	
		btn1.connect("clicked",self.on_clicked)
		self.add(fixed)
		self.add(entry)
		self.show_all()
	
sdnmanager()
gtk.main()	
