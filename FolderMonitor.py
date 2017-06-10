import os
import time
import logging
import sys
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from properties.p import Property

class Event(LoggingEventHandler):   

    def on_modified(self, event):
        os.system(str_schedule_app)
        logging.debug(str(event))
        
class fileHandler:
    
    def __init__(self):
        
        prop = Property()
        self.propertyFile = sys.argv[1] if len(sys.argv) > 1 else ''
        logging.debug(self.propertyFile)
        
        if not(os.path.exists(self.propertyFile)): #if file does not exist
            raise OSError("Property file not found! Please provide property file as an argument.")
    
        #Load the property file
        self.dic_prop = prop.load_property_files(self.propertyFile)
    
    def getPropertyFile(self):
        return self.propertyFile
        
    def getPropertyAttr(self):
        return self.dic_prop

if __name__ == "__main__":
    
    try:
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
                        
        fileH = fileHandler()
        dp = fileH.getPropertyAttr()
        
        #Pick the location from properties file: folder to watch and application to run
        str_input_folder_monitor = dp['watch_folder']
        str_schedule_app = dp['scheduleApplication']
		
        print("Input Folder to be Monitored:" + str_input_folder_monitor ) #logging.debug(
        print("Executable to be called:" + str_schedule_app )
		
        event_handler = Event()
        observer = Observer()
        observer.schedule(event_handler, str_input_folder_monitor, recursive=True)
        observer.start()
        
        while True: 
            time.sleep(1)
            
    except OSError as E:
        logging.debug("OS Error: "+str(E.args[0]))
    
    except KeyboardInterrupt:
        observer.stop()
        observer.join()        
        
    except Exception as E:
        logging.debug("Exception: "+str(E.args))