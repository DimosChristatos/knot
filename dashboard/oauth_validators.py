# Copyright [2019] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings
from oauth2_provider.oauth2_validators import OAuth2Validator

from .models import User


class CustomOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self, request):
        user = User.objects.get(pk=request.user.pk)

        return {
            'sub': user.username,
            'preferred_username': user.username,
            'email': user.email,
            'name': user.get_full_name(),
            'given_name': user.first_name,
            'family_name': user.last_name,
            'karvdash_namespace': user.namespace,
            'karvdash_ingress_url': settings.INGRESS_URL,
            'karvdash_registry_url': settings.HARBOR_URL,
            'karvdash_argo_workflows_url': settings.ARGO_WORKFLOWS_URL
        }
