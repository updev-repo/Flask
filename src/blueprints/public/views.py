import operator
from datetime import datetime, timedelta
from flask import (Blueprint, render_template, redirect, flash, url_for,
                   make_response, request, send_from_directory,current_app)
from flask_sqlalchemy import Pagination
from flask_login import current_user
from .forms import *
from models import *
from blueprints.account.forms import ContactForm


public = Blueprint('public', __name__, url_prefix='')



def return_xml(view, **kwargs):
    data = render_template(view, **kwargs)
    response = make_response(data)
    response.headers["Content-Type"] = "application/xml"
    return response

@public.route('/', methods=["GET" , "POST"])
def index():
    setting = LandingSetting.query.first()
    logo = SiteLogo.query.first()
    banner = BackgroundImage.query.first()
    items = Section.query.filter(Section.type=='Faq').first()
    if request.method=="POST":
        email = request.form['email']
        name = request.form['name']
        message = request.form['message']
        subject = request.form['subject']
        contact_message = ContactMessage(
                    name=name,
                    email=email,
                    text=message
        )
        db.session.add(contact_message)
        db.session.commit()
        flash('Message delivered successfully added')
    return render_template('public/index.html',setting=setting, faq=faq, logo=logo, banner=banner)


@public.route("/robots.txt", methods=["GET"])
def robots():
    return send_from_directory(current_static_folder, 'robots.txt')


def return_xml(view, **kwargs):
    data = render_template(view, **kwargs)
    response = make_response(data)
    response.headers["Content-Type"] = "application/xml"
    return response

def routes():
    rules = []
    for rule in current_url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            methods = ','.join(sorted(rule.methods))
            rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    routes = []
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        if 'public.' in endpoint or 'seo' in endpoint:
            route = {'endpoint': endpoint, 'methods': methods, 'rule': rule}
            routes.append(route)
    return routes


def sitemap_date(val):
    return datetime.date(val)

"""@sitemaps.route('/sitemap.xml')
def index():
    sitemaps_list = [
        {'loc': url_for('public.main_xml', _external=True)},
        {'loc': url_for('public.blog_xml', _external=True)},
    ]
    return return_xml('public/sitemapindex.html', sitemaps=sitemaps_list)

@sitemaps.route('/main.xml')
def main_xml():
    urlset = []
    ten_days_ago = datetime.now() - timedelta(days=10)
    for route in routes():
        urlset.append({'loc': url_for(route['endpoint'], _external=True),
                       'lastmod': '{}'.format(sitemap_date(ten_days_ago)),
                       'changefreq': 'daily'})
    return return_xml('public/sitemap.html', urlset=urlset)


@sitemaps.route('/blog.xml')
def blog_xml():
    urlset = []
    blog = BlogPost.query.all()
    for item in blog:
        urlset.append({'loc': url_for('blog.blog_article', article_id=item.id,  _external=True),
                       'lastmod': '{}'.format(sitemap_date(item.updated_at) if blog.updated_at is not None else ''),
                       'changefreq': 'daily'})
    return return_xml('public/sitemap.html', urlset=urlset)
"""

@public.route('/about-us')
def about():
    setting = LandingSetting.query.first()
    logo = SiteLogo.query.first()
    item = Section.query.filter(Section.type=="About").first()
    return render_template('public/about.html',  items=item,setting=setting, logo=logo)


@public.route('/contact', methods=['GET', 'POST'])
def contact():
    logo = SiteLogo.query.first()
    setting = LandingSetting.query.first()
    if current_user.is_authenticated:
        form = ContactForm()
    else:
        form = PublicContactForm()
    editable_html_obj = EditableHTML.get_editable_html('contact')
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.is_authenticated:
                contact_message = ContactMessage(
                    user_id=current_user.id,
                    text=form.text.data
                )
            else:
                contact_message = ContactMessage(
                    name=form.name.data,
                    email=form.email.data,
                    text=form.text.data
                )
            db.session.add(contact_message)
            db.session.commit()
            #flash('Successfully sent contact message.', 'success')
            return {'text':'Successfully sent contact message.'}
    return render_template('public/contact.html', editable_html_obj=editable_html_obj, form=form,setting=setting, logo=logo)


@public.route('/privacy')
def privacy():
    logo = SiteLogo.query.first()
    setting = LandingSetting.query.first()
    items = Section.query.filter(Section.type=='privacy').first()
    print(items)
    return render_template('public/privacy.html', items = items,setting=setting, logo=logo)



@public.route('/faq')
def faq():
    logo = SiteLogo.query.first()
    setting = LandingSetting.query.first()
    items = Section.query.filter(Section.type=='Faq').first()
    return render_template('public/faq.html', items=items, setting=setting, logo=logo)



@public.route('/terms')
def terms():
    logo = SiteLogo.query.first()
    setting = LandingSetting.query.first()
    items = Section.query.filter(Section.type=='Terms').first()
    return render_template('public/terms.html', items=items, setting=setting, logo=logo)




   