from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

myapp = Flask("SuperScrapper")

fk_db = {}

@myapp.route("/")
def home():
  return render_template("make_web.html")

@myapp.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower() 
    existingJobs = fk_db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      fk_db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", 
  searchingBy=word, 
  resultNumber=len(jobs),
  jobs=jobs
  )

@myapp.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = fk_db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")
myapp.run(host="0.0.0.0")
