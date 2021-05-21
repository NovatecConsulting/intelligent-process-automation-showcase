/*
 * Copyright 2021 original authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package novatec.poc.ipa.intelligent;

import io.micronaut.runtime.event.annotation.EventListener;
import io.micronaut.runtime.server.event.ServerStartupEvent;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.ExecuteOn;
import org.camunda.bpm.engine.RuntimeService;

import javax.inject.Singleton;

@Singleton
public class IntelligentProcessInstanceCreator {

    private final RuntimeService runtimeService;

    public IntelligentProcessInstanceCreator(RuntimeService runtimeService) {
        this.runtimeService = runtimeService;
    }

    @EventListener
    @ExecuteOn(TaskExecutors.IO)
    public void onApplicationEvent(ServerStartupEvent event) {
        runtimeService.startProcessInstanceByKey("costs_submission_intelligent", "IntelligentOnStartup");
    }
}