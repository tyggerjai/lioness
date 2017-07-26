#########
# Scheduler for bot cron jobs
#######
import time
from pytz import timezone
import parsedatetime.parsedatetime as pdt
import datetime

class Scheduler():
    def __init__(self, **kwargs):
        self.dbconn = kwargs["dbconn"]
        self.log = kwargs["log"]
        self.cal = pdt.Calendar()
        self.joblist = self.get_joblist()

    def get_joblist(self):

        resp = self.dbconn.query("""SELECT * from reminders WHERE `complete` NOT LIKE 'TRUE' ORDER BY jobtime""", () )
        
        self.log.critical(resp)
        return resp 
    def job_done(self, jobid):
        print("Marked {} As done".format(jobid))
        resp = self.dbconn.query("""UPDATE `reminders` SET `complete` = "TRUE" WHERE `reminderID`  = %s """, (jobid,) )
        
        self.log.critical(resp)
    
    def get_next_job(self):
        # jobs should have a job ID
        resp = self.dbconn.query("""SELECT `jobtime`, `reminderID`, `job`, `args` from reminders WHERE `complete` IS NULL ORDER BY `jobtime` LIMIT 1 """, () )
        self.log.critical("NEXT JOB")
        self.log.critical(resp)
        job = dict()
        if len(resp) > 0:
            job["time"] = resp[0][0]
            job["id"] = resp[0][1]
        return job
        
    def do_jobs(self):
        todo = list()
        for job in self.joblist:
             if (job[3] < datetime.datetime.now()):
                self.log.critical("Job {} time: {}".format(job[4], datetime.datetime.now() - job[3]))
          
                todo.append(job[4])
        self.joblist = [job for job in self.joblist if job not in todo]

        return todo
