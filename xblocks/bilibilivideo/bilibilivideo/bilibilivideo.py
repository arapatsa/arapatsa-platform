#!/usr/bin/python
# -*- coding: utf-8 -*-

"""TO-DO: Write a description of what this XBlock is."""

import os
import pkg_resources
from django.template import Context
from django.utils.translation import ugettext as _
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer, Dict
from xblock.fragment import Fragment

from xblockutils.resources import ResourceLoader


class BilibiliVideoXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    loader = ResourceLoader(__name__)

    icon_class = "video"

    # TO-DO: delete count, and define your own fields.
    display_name = String(
        display_name=_("Display Name"),
        default="Bilibili Video",
        scope=Scope.settings,
        help=_("The display name for this component."),
    )
    embed_code = String(
        display_name=_("Embed Code"),
        help=_(
            "Bilibili provides an embed code for video. To get embed_code for video, hover/click on share icon of video "
            "and click on embed code, paster into this field."
        ),
        scope=Scope.settings,
        default="",
    )

    def load_resource(self, resource_path):  # pylint: disable=no-self-use
        """
        Gets the content of a resource
        """

        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return resource_content.decode("utf-8")

    def render_template(self, path, context=None):
        """
        Evaluate a template by resource path, applying the provided context
        """

        return self.loader.render_django_template(
            os.path.join("static/html", path),
            context=Context(context or {}),
            i18n_service=self.runtime.service(self, "i18n"),
        )

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers/instructors when editing the XBlock.
        """

        context = {"display_name": self.display_name, "embed_code": self.embed_code}
        html = self.render_template("studio_edit.html", context)
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/studio_edit.js"))
        frag.initialize_js("BilibiliVideoXBlockEdit")
        return frag

    @XBlock.json_handler
    def save_settings(self, data, suffix=""):
        """
        The saving handler.
        """
        self.display_name = data.get("display_name", self.display_name)
        self.embed_code = data.get("embed_code", self.embed_code)
        return {"result": "success"}

    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students when viewing courses.
        """
        context = {"display_name": self.display_name, "embed_code": self.embed_code}
        html = self.render_template("bilibilivideo.html", context)
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/bilibilivideo.css"))
        # frag.add_javascript(self.load_resource("static/js/bilibilivideo.js"))
        frag.initialize_js("BilibiliVideoXBlock")
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            (
                "BilibiliVideoXBlock",
                """<bilibilivideo/>
             """,
            ),
            (
                "Multiple BilibiliVideoXBlock",
                """<vertical_demo>
                <bilibilivideo/>
                <bilibilivideo/>
                <bilibilivideo/>
                </vertical_demo>
             """,
            ),
        ]
