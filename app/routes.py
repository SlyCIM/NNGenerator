from app import app, db
from app.models import Task, AnalysisTask
from flask import render_template, redirect, flash, jsonify, send_from_directory, request
from app.forms import GeneratorForm, GeneratorTestCaseForm
from app import utils
from threading import Thread
import math
import os


@app.route("/generate_for_analysis")
def generate_for_analysis():
    return render_template("generate_for_analysis.html", title="Generator - Generate for analysis")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html", title="Generator - Analysis")


@app.route("/analysis_g_const", methods=['GET', 'POST'])
def analysis_g_const():
    if request.method == 'POST':
        im_path1, im_path2, im_path3, im_path4 = None, None, None, None
        uploaded_files = request.files.getlist("file1[]")
        if uploaded_files:
            im_path1, meta_info = utils.make_plot(uploaded_files, 'g', 'm', "Число омматидиев", "Число коллизий")
        uploaded_files = request.files.getlist("file2[]")
        if uploaded_files:
            im_path2, meta_info = utils.make_plot(uploaded_files, 'g', 'h', "Расстояние между глазами", "Число коллизий")
        uploaded_files = request.files.getlist("file3[]")
        if uploaded_files:
            im_path3, meta_info = utils.make_plot(uploaded_files, 'g', 'l', "Радиус глаза", "Число коллизий")
        uploaded_files = request.files.getlist("file4[]")
        if uploaded_files:
            im_path4, meta_info = utils.make_plot(uploaded_files, 'g', 'rMax', "Максимальное расстояние до объекта",
                                             "Число коллизий")
        meta_dict = {}
        if meta_info:
            meta_dict = {'gObj': f'{meta_info[3]}..{meta_info[4]}',
                         'fiObj': f'{meta_info[5]}..{meta_info[6]}',
                         'rObj': f'{meta_info[7]}..{meta_info[8]}' if not im_path4 else f'{meta_info[7]}..',
                         'n': meta_info[9]}
        return render_template("analysis_result_g_const.html", title="Generator - Analysis", im_path1=im_path1,
                               im_path2=im_path2, im_path3=im_path3, im_path4=im_path4, meta_dict=meta_dict)
    return render_template("analysis_result_g_const.html", title="Generator - Analysis")


@app.route("/analysis_g_const_m_diff", methods=['GET', 'POST'])
def analysis_g_const_m_diff():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        im_path, meta_info = utils.make_plot(uploaded_files, 'g', 'm', "Число омматидиев", "Число коллизий")
        meta_dict = {}
        if meta_info:
            meta_dict = {'h': meta_info[0], 'l': meta_info[1], 'gObj': f'{meta_info[3]}..{meta_info[4]}',
                         'fiObj': f'{meta_info[5]}..{meta_info[6]}', 'rObj': f'{meta_info[7]}..{meta_info[8]}',
                         'n': meta_info[9]}
        return render_template("analysis_result.html", title="Generator - Analysis", im_path=im_path,
                               meta_dict=meta_dict)
    return render_template("analysis_result.html", title="Generator - Analysis")


@app.route("/analysis_g_const_h_diff", methods=['GET', 'POST'])
def analysis_g_const_h_diff():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        im_path, meta_info = utils.make_plot(uploaded_files, 'g', 'h', "Расстояние между глазами", "Число коллизий")
        meta_dict = {}
        if meta_info:
            meta_dict = {'l': meta_info[1],'m': meta_info[2], 'gObj': f'{meta_info[3]}..{meta_info[4]}',
                         'fiObj': f'{meta_info[5]}..{meta_info[6]}', 'rObj': f'{meta_info[7]}..{meta_info[8]}',
                         'n': meta_info[9]}
        return render_template("analysis_result.html", title="Generator - Analysis", im_path=im_path,
                               meta_dict=meta_dict)
    return render_template("analysis_result.html", title="Generator - Analysis")


@app.route("/analysis_g_const_l_diff", methods=['GET', 'POST'])
def analysis_g_const_l_diff():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        im_path, meta_info = utils.make_plot(uploaded_files, 'g', 'l', "Радиус глаза", "Число коллизий")
        meta_dict = {}
        if meta_info:
            meta_dict = {'h': meta_info[0], 'm': meta_info[2], 'gObj': f'{meta_info[3]}..{meta_info[4]}',
                         'fiObj': f'{meta_info[5]}..{meta_info[6]}', 'rObj': f'{meta_info[7]}..{meta_info[8]}',
                         'n': meta_info[9]}
        return render_template("analysis_result.html", title="Generator - Analysis", im_path=im_path,
                               meta_dict=meta_dict)
    return render_template("analysis_result.html", title="Generator - Analysis")


@app.route("/analysis_g_const_r_diff", methods=['GET', 'POST'])
def analysis_g_const_r_diff():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        im_path, meta_info = utils.make_plot(uploaded_files, 'g', 'rMax', "Максимальное расстояние до объекта",
                                             "Число коллизий")
        meta_dict = {}
        if meta_info:
            meta_dict = {'h': meta_info[0], 'l': meta_info[1], 'm':meta_info[2], 'gObj': f'{meta_info[3]}..{meta_info[4]}',
                         'fiObj': f'{meta_info[5]}..{meta_info[6]}', 'rObj': f'{meta_info[7]}..',
                         'n': meta_info[9]}
        return render_template("analysis_result.html", title="Generator - Analysis", im_path=im_path,
                               meta_dict=meta_dict)
    return render_template("analysis_result.html", title="Generator - Analysis")


@app.route("/g_const_m_diff", methods=['GET', 'POST'])
def g_const_m_diff():
    form = GeneratorForm()
    if form.validate_on_submit():
        h = float(form.h.data)
        l = float(form.l.data)
        if l >= h:
            flash('"l" must be less than "h"')
            return render_template("g_const_m_diff.html", title="Generator - Generation", form=form)
        fi_min = float(form.fi_min.data)
        fi_max = float(form.fi_max.data)
        r_min = float(form.r_min.data)
        r_max = float(form.r_max.data)
        n = int(form.n.data)
        m_start = int(request.form.get('m_start'))
        m_finish = int(request.form.get('m_finish'))
        m_step = int(request.form.get('m_step'))
        tasks = []
        an_task = AnalysisTask()
        db.session.add(an_task)
        db.session.commit()
        for i in range(m_start, m_finish + 1, m_step):
            task = Task(produced=0, target=n, dataset_size=i, dataset_filename='', analysis_id=an_task.id)
            db.session.add(task)
            db.session.commit()
            tasks.append({'id': task.id, 'diff_item': task.dataset_size})
        g_list = [int(request.form.get('g1')), int(request.form.get('g2')), int(request.form.get('g3')),
                  int(request.form.get('g4')), int(request.form.get('g5')), int(request.form.get('g6'))]
        thread = Thread(target=utils.generate_const_g_diff_m, args=(h, l, n, r_min, r_max, fi_min, fi_max, g_list, tasks))
        thread.start()
        return redirect(f'/progress_generation_for_analysis/{an_task.id}')
    return render_template("g_const_m_diff.html", title="Generator - Generate for analysis", form=form)


@app.route("/g_const_l_diff", methods=['GET', 'POST'])
def g_const_l_diff():
    form = GeneratorForm()
    if form.validate_on_submit():
        m = int(form.m.data)
        h = float(form.h.data)
        fi_min = float(form.fi_min.data)
        fi_max = float(form.fi_max.data)
        r_min = float(form.r_min.data)
        r_max = float(form.r_max.data)
        n = int(form.n.data)
        l_start = int(request.form.get('l_start'))
        l_finish = int(request.form.get('l_finish'))
        l_step = int(request.form.get('l_step'))
        tasks = []
        an_task = AnalysisTask()
        db.session.add(an_task)
        db.session.commit()
        for i in range(l_start, l_finish + 1, l_step):
            task = Task(produced=0, target=n, dataset_size=m, dataset_filename='', analysis_id=an_task.id)
            db.session.add(task)
            db.session.commit()
            tasks.append({'id': task.id, 'diff_item': i})
        g_list = [int(request.form.get('g1')), int(request.form.get('g2')), int(request.form.get('g3')),
                  int(request.form.get('g4')), int(request.form.get('g5')), int(request.form.get('g6'))]
        thread = Thread(target=utils.generate_const_g_diff_l,
                        args=(m, h, n, r_min, r_max, fi_min, fi_max, g_list, tasks))
        thread.start()
        return redirect(f'/progress_generation_for_analysis/{an_task.id}')
    return render_template("g_const_l_diff.html", title="Generator - Generate for analysis", form=form)


@app.route("/g_const_h_diff", methods=['GET', 'POST'])
def g_const_h_diff():
    form = GeneratorForm()
    if form.validate_on_submit():
        m = int(form.m.data)
        l = float(form.l.data)
        fi_min = float(form.fi_min.data)
        fi_max = float(form.fi_max.data)
        r_min = float(form.r_min.data)
        r_max = float(form.r_max.data)
        n = int(form.n.data)
        h_start = int(request.form.get('h_start'))
        h_finish = int(request.form.get('h_finish'))
        h_step = int(request.form.get('h_step'))
        tasks = []
        an_task = AnalysisTask()
        db.session.add(an_task)
        db.session.commit()
        for i in range(h_start, h_finish + 1, h_step):
            task = Task(produced=0, target=n, dataset_size=m, dataset_filename='', analysis_id=an_task.id)
            db.session.add(task)
            db.session.commit()
            tasks.append({'id': task.id, 'diff_item': i})
        g_list = [int(request.form.get('g1')), int(request.form.get('g2')), int(request.form.get('g3')),
                  int(request.form.get('g4')), int(request.form.get('g5')), int(request.form.get('g6'))]
        thread = Thread(target=utils.generate_const_g_diff_h,
                        args=(m, l, n, r_min, r_max, fi_min, fi_max, g_list, tasks))
        thread.start()
        return redirect(f'/progress_generation_for_analysis/{an_task.id}')
    return render_template("g_const_h_diff.html", title="Generator - Generate for analysis", form=form)


@app.route("/g_const_r_diff", methods=['GET', 'POST'])
def g_const_r_diff():
    form = GeneratorForm()
    if form.validate_on_submit():
        m = int(form.m.data)
        h = float(form.h.data)
        fi_min = float(form.fi_min.data)
        fi_max = float(form.fi_max.data)
        r_min = float(form.r_min.data)
        l = int(form.l.data)
        n = int(form.n.data)
        r_start = int(request.form.get('r_start'))
        r_finish = int(request.form.get('r_finish'))
        r_step = int(request.form.get('r_step'))
        tasks = []
        an_task = AnalysisTask()
        db.session.add(an_task)
        db.session.commit()
        for i in range(r_start, r_finish + 1, r_step):
            task = Task(produced=0, target=n, dataset_size=m, dataset_filename='', analysis_id=an_task.id)
            db.session.add(task)
            db.session.commit()
            tasks.append({'id': task.id, 'diff_item': i})
        g_list = [int(request.form.get('g1')), int(request.form.get('g2')), int(request.form.get('g3')),
                  int(request.form.get('g4')), int(request.form.get('g5')), int(request.form.get('g6'))]
        thread = Thread(target=utils.generate_const_g_diff_r,
                        args=(m, l, n, r_min, h, fi_min, fi_max, g_list, tasks))
        thread.start()
        return redirect(f'/progress_generation_for_analysis/{an_task.id}')
    return render_template("g_const_r_diff.html", title="Generator - Generate for analysis", form=form)


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
        # if form.object_on_y_axis.data:
        #     fi_min = math.pi / 2
        #     fi_max = math.pi / 2
        # if form.fix_g.data:
        #     fi_min = math.pi / 4
        #     fi_max = math.pi - fi_min
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
        task = Task(produced=0, target=n, dataset_size=m, dataset_filename='')
        db.session.add(task)
        db.session.commit()
        thread = Thread(target=utils.generate_usual_way, args=(h, l, m, n, r_min, r_max, fi_min, fi_max, g_min, g_max, task.id))
        thread.start()
        return redirect(f'/progress/{task.id}')
    return render_template("generator_page.html", title="Generator - Generation", form=form)


@app.route('/generate_test_case', methods=['GET', 'POST'])
def generator_test_case():
    form = GeneratorTestCaseForm()
    if form.validate_on_submit():
        try:
            h = float(form.h.data)
        except ValueError:
            flash('"h" must be real number', 'h')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if h <= 0:
            flash('"h" must be positive real number', 'h')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            l = float(form.l.data)
        except ValueError:
            flash('"l" must be real number', 'l')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if l <= 0:
            flash('"l" must be positive real number', 'l')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if l >= h:
            flash('"l" must be less than "h"')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            m = int(form.m.data)
        except ValueError:
            flash('"m" must be integer number', 'm')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if m <= 3:
            flash('"m" must be more than 3', 'm')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            x_start = float(form.x_start.data)
        except ValueError:
            flash('"x_start" must be real number', 'x_start')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            y_start = float(form.y_start.data)
        except ValueError:
            flash('"y_start" must be real number', 'y_start')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if y_start < 0:
            flash('"y_start" must be positive real number', 'y_start')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            x_end = float(form.x_end.data)
        except ValueError:
            flash('"x_end" must be real number', 'x_end')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            y_end = float(form.y_end.data)
        except ValueError:
            flash('"y_end" must be real number', 'y_end')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if y_end <= 0:
            flash('"y_end" must be positive real number', 'y_end')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if y_end == y_start:
            flash('"y_end" and "y_start" must be different', 'y_end')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if x_end == x_start:
            flash('"x_end" and "x_start" must be different', 'x_end')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)

        try:
            n = int(form.n.data)
        except ValueError:
            flash('"n" must be integer number', 'n')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        if n <= 0:
            flash('"m" must be positive integer number', 'n')
            return render_template("generator_test_case.html", title="Generator - Generation", form=form)
        task = Task(produced=0, target=n, dataset_size=m, dataset_filename='')
        db.session.add(task)
        db.session.commit()
        thread = Thread(target=utils.generate_test_case, args=(h, l, m, n, x_start, x_end, y_start, y_end, task.id))
        thread.start()
        return redirect(f'/progress/{task.id}')
    return render_template("generator_test_case.html", title="Generator - Generation", form=form)


@app.route('/progress_generation_for_analysis/<task_id>')
def progress_generation_for_analysis(task_id):
    return render_template('progress_generation_for_analysis.html', title="Generator - Progress of generation",
                           task_id=task_id)


@app.route('/progress/<task_id>')
def progress(task_id):
    return render_template('progress.html', title="Generator - Progress of generation", task_id=task_id)


@app.route('/task_info/<task_id>')
def get_task_info(task_id):
    task = Task.query.get(task_id)
    return jsonify({'produced': task.produced, 'target': task.target, 'dataset_size': task.dataset_size,
                    'task_id': task.id})


@app.route('/analysis_task_info/<task_id>')
def analysis_task_info(task_id):
    main_task = AnalysisTask.query.get(task_id)
    produced = 0
    target = 0
    for task in Task.query.filter_by(analysis_id=main_task.id).all():
        produced += task.produced
        target += task.target
    return jsonify({'produced': produced, 'target': target * 6, 'task_id': main_task.id})


@app.route('/dataset/<task_id>')
def get_dataset(task_id):
    path = os.path.join(app.root_path, 'datasets')
    return send_from_directory(path, filename=f'dataset_{task_id}.csv', as_attachment=True)


@app.route('/clean_dataset', methods=['GET', 'POST'])
def clean_dataset():
    if request.method == 'POST':
        uploaded_file = request.files.get("file")
        #im_path, meta_info = utils.make_plot(uploaded_files, 'g', 'l', "Радиус глаза", "Число коллизий")
        # meta_dict = {}
        # if meta_info:
        #     meta_dict = {'h': meta_info[0], 'm': meta_info[2], 'gObj': f'{meta_info[3]}..{meta_info[4]}',
        #                  'fiObj': f'{meta_info[5]}..{meta_info[6]}', 'rObj': f'{meta_info[7]}..{meta_info[8]}',
        #                  'n': meta_info[9]}
        # return render_template("analysis_result.html", title="Generator - Analysis", im_path=im_path,
        #                        meta_dict=meta_dict)
        dataset_name = utils.clean_dataset(uploaded_file)
        return send_from_directory(os.path.join(app.root_path, 'datasets'), filename=dataset_name, as_attachment=True)
    else:
        return render_template('clean_dataset.html', title="Generator - Clean datasets")
    # path = os.path.join(app.root_path, 'datasets')
    # return send_from_directory(path, filename=f'dataset_{task_id}.csv', as_attachment=True)