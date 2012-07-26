from plone.testing import z2

from plone.app.testing import *
import collective.captionmanager

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.captionmanager,
                                additional_z2_products=[],
                                gs_profile_id='collective.captionmanager:default',
                                name="collective.captionmanager:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.captionmanager:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.captionmanager:Functional")

