# Use the official image as a parent image.
FROM camunda/camunda-bpm-platform:run-7.15.0-alpha4

# Set the working directory.
WORKDIR /camunda

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 8080

# Copy the rest of your app's source code from your host to your image filesystem.
COPY /lib/activation-1.1.jar /camunda/configuration/userlib
COPY /lib/camunda-bpm-mail-core-1.3.0.jar /camunda/configuration/userlib
COPY /lib/camunda-connect-connectors-all-1.5.0.jar /camunda/configuration/userlib
COPY /lib/camunda-connect-core-1.5.0.jar /camunda/configuration/userlib
COPY /lib/camunda-commons-logging-1.10.0.jar /camunda/configuration/userlib
COPY /lib/camunda-commons-utils-1.10.0.jar /camunda/configuration/userlib
COPY /lib/camunda-engine-plugin-connect-7.14.0.jar /camunda/configuration/userlib
COPY /lib/camunda-template-engines-freemarker-2.0.0.jar /camunda/configuration/userlib
COPY /lib/freemarker-2.3.29.jar /camunda/configuration/userlib
COPY /lib/groovy-all-2.4.13.jar /camunda/configuration/userlib
COPY /lib/javax.mail-1.5.5.jar /camunda/configuration/userlib
COPY /lib/slf4j-api-2.0.0-alpha1.jar /camunda/configuration/userlib

# Copy the file to classpath
COPY /config/mail-config.properties /camunda/configuration/userlib

COPY /resources/processes/costs_submission_manual.bpmn /camunda/configuration/resources
COPY /resources/processes/costs_submission_intelligent.bpmn /camunda/configuration/resources
COPY /resources/html/task-form.html /camunda/configuration/resources
COPY /resources/html/upload-form.html /camunda/configuration/resources

ENTRYPOINT ["./camunda.sh"]