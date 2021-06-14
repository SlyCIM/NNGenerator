from app import app, db
from app.models import Task
from flask import render_template, redirect, flash, jsonify
from app.forms import GeneratorForm
from app import utils
from threading import Thread
import math


@app.route("/")
def home():
    return render_template("index.html", title="Generator - Home page")


@app.route('/generate', methods=['GET', 'POST'])
def generator_page():
    form = GeneratorForm()
    if form.validate_on_submit():
        try:
            h = float(form.h.data)
        except ValueError:
            flash('"h" must be real number', 'h')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if h <= 0:
            flash('"h" must be positive real number', 'h')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            l = float(form.l.data)
        except ValueError:
            flash('"l" must be real number', 'l')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if l <= 0:
            flash('"l" must be positive real number', 'l')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if l >= h:
            flash('"l" must be less than "h"')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            m = int(form.m.data)
        except ValueError:
            flash('"m" must be integer number', 'm')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if m <= 3:
            flash('"m" must be more than 3', 'm')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            g_min = float(form.g_min.data)
        except ValueError:
            flash('"g_min" must be real number', 'g_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if g_min <= 0:
            flash('"g_min" must be positive real number', 'g_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            g_max = float(form.g_max.data)
        except ValueError:
            flash('"g_max" must be real number', 'g_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if g_max <= 0:
            flash('"g_max" must be positive real number', 'g_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if g_max < g_min:
            flash('"g_max" must be more than "g_min"', 'g_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if form.fix_g.data:
            g_min = 2
            g_max = 4

        try:
            fi_min = float(form.fi_min.data)
        except ValueError:
            flash('"fi_min" must be real number', 'fi_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if fi_min < 0:
            flash('"fi_min" must be more than 0', 'fi_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            fi_max = float(form.fi_max.data)
        except ValueError:
            flash('"fi_max" must be real number', 'fi_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if fi_max <= 0:
            flash('"fi_max" must be positive real number', 'fi_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if fi_max <= fi_min:
            flash('"fi_max" must be more than "fi_min"', 'fi_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if fi_max > math.pi:
            flash('"fi_max" must be less than 3.14', 'fi_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if form.object_on_y_axis.data:
            fi_min = math.pi / 2
            fi_max = math.pi / 2
        if form.fix_g.data:
            fi_min = math.pi / 4
            fi_max = math.pi - fi_min
        try:
            r_min = float(form.r_min.data)
        except ValueError:
            flash('"r_min" must be real number', 'r_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if r_min <= 0:
            flash('"r_min" must be positive real number', 'r_min')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            r_max = float(form.r_max.data)
        except ValueError:
            flash('"r_max" must be real number', 'r_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if r_max <= 0:
            flash('"r_max" must be positive real number', 'r_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if r_max <= r_min:
            flash('"r_max" must be more tham "r_min"', 'r_max')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            n = int(form.n.data)
        except ValueError:
            flash('"n" must be integer number', 'n')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if n <= 0:
            flash('"m" must be positive integer number', 'n')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            lambd = float(form.lambd.data)
        except ValueError:
            flash('"lambd" must be real number', 'lambd')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if lambd <= 0:
            flash('"lambd" must be positive real number', 'lambd')
            return render_template("generator_page.html", title="Generator - Generation", form=form)

        try:
            gamma = float(form.gamma.data)
        except ValueError:
            flash('"gamma" must be real number', 'gamma')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        if gamma <= 0:
            flash('"gamma" must be positive real number', 'gamma')
            return render_template("generator_page.html", title="Generator - Generation", form=form)
        task = Task(produced=0, target=n, dataset_size=m)
        db.session.add(task)
        db.session.commit()
        thread = Thread(target=utils.generate, args=(h, l, m, n, r_min, r_max, fi_min, fi_max, g_min, g_max, lambd,
                                                     gamma, task.id, form.add.data))
        thread.start()
        return redirect(f'/progress/{task.id}')
    return render_template("generator_page.html", title="Generator - Generation", form=form)


@app.route('/progress/<task_id>')
def progress(task_id):
    return render_template('progress.html', title="Generator - Progress of generation", task_id=task_id)


@app.route('/task_info/<task_id>')
def get_task_info(task_id):
    task = Task.query.get(task_id)
    return jsonify({'produced': task.produced, 'target': task.target, 'dataset_size': task.dataset_size})