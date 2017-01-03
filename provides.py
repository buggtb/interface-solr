#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in  writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import not_unless
from charmhelpers.core.hookenv import log

class SolrProvides(RelationBase):
    scope = scopes.SERVICE

    @hook('{provides:solr-interface}-relation-joined')
    def joined(self):
        log("solr-interface-joined")
        conversation = self.conversation()
        conversation.set_state('{relation_name}.core.requested')

    @hook('{provides:solr-interface}-relation-{broken,departed}')
    def departed(self):
        log("solr-interface-broken")
        conversation = self.conversation()
        conversation.remove_state('{relation_name}.core.requested')

    @not_unless('{provides:solr-interface}.core.requested')
    def provide_core(self, service, host, port, core):
        log("solr-interface-core-requested")
        conversation = self.conversation(scope=service)
        conversation.set_remote(
            host=host,
            port=port,
            core=core,
        )
        conversation.set_local('core', core)
        conversation.remove_state('{relation_name}.core.requested')

    def requested_cores(self):
        for conversation in self.conversations():
            service = conversation.scope
            yield service
