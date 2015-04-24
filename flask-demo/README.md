# Flask on Google App Engine demo

This is an example of using the [Flask framework](http://flask.pocoo.org/) on [Google App Engine](https://cloud.google.com/appengine/). I used this in the talk [Building Scalable Web Apps with Python and Google Cloud Platform](http://www.oreilly.com/pub/e/3388). See [the book's website](http://ae-book.appspot.com/code#Webcasts) for links to slides and video.

```
virtualenv venv
source venv/bin/activate

cd flask-demo
pip install -r requirements_cfg.txt
pip install -t lib -r requirements_vnd.txt
```

To run a GAE development server:

```
gcloud preview app run app.yaml
```

To deploy to GAE:

```
gcloud preview app deploy app.yaml
```

(When `gcloud app` graduates from its preview release, use `gcloud app` instead of `gcloud preview app`.)

To run tests:

```
python tests.py
```
