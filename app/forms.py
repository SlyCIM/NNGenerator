# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
import math


class GeneratorForm(FlaskForm):
    h = StringField("Distance between the center of the coordinate system and the center of the facet eye (mm)",
                    default='80')
    l = StringField("Facet eye radius (mm)", default='20')
    m = StringField("The number of ommatidia in the facet eye", default='100')
    g_min = StringField("Minimal radius of the object (mm)", default='2')
    g_max = StringField("Maximal radius of the object (mm)", default='200')
    fi_min = StringField("Minimal azimuth of the object (rad, > 0)", default='0')
    fi_max = StringField("Maximal azimuth of the object (rad, < 3.14)", default=f'{math.pi}')
    r_min = StringField("Minimal distance between the center of the coordinate system and the center of the object (mm)",
                    default='40')
    r_max = StringField("Maximal distance between the center of the coordinate system and the center of the object (mm)",
                    default='2000')
    n = StringField("Number of precedents to generate", default='10000')
    object_on_y_axis = BooleanField('Fix object on Y axis')


class GeneratorTestCaseForm(FlaskForm):
    h = StringField("Distance between the center of the coordinate system and the center of the facet eye (mm)",
                    validators=[DataRequired()], default='80')
    l = StringField("Facet eye radius (mm)", validators=[DataRequired()], default='20')
    m = StringField("The number of ommatidia in the facet eye", validators=[DataRequired()], default='100')
    x_start = StringField("X of start point", validators=[DataRequired()])
    y_start = StringField("Y of start point", validators=[DataRequired()])
    x_end = StringField("X of end point", validators=[DataRequired()])
    y_end = StringField("Y of end point", validators=[DataRequired()])
    n = StringField("Number of precedents to generate", validators=[DataRequired()], default='1000')
