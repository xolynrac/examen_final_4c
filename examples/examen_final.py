# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Provide a 'Big Bank' example.

Illustrate how to create a software architecture diagram using code, based on
https://github.com/structurizr/dsl/blob/master/examples/big-bank-plc.dsl.
"""


import logging

from structurizr import Workspace
from structurizr.model import Enterprise, Location, Tags
from structurizr.view import ElementStyle, PaperSize, RelationshipStyle, Shape


def main():
    """Standard entry point for examples.  Do not rename."""
    return create_big_bank_workspace()


def create_big_bank_workspace():
    """Create the big bank example."""

    workspace = Workspace(
        name="SCV",
        description=(
            "Sistema de Clinica Veterinaria"
        ),
    )

    existing_system_tag = "Existing System"
    business_staff_tag = "Bank Staff"
    web_browser_tag = "Web Browser"
    mobile_app_tag = "Mobile App"
    database_tag = "Database"
    failover_tag = "Failover"
    bounded_context_tag = "Bounded Context"

    model = workspace.model
    views = workspace.views

    model.enterprise = Enterprise(name="Veterinaria Mi Mascota Feliz")

    # people and software systems
    cliente = model.add_person(
        location=Location.External,
        name="Cliente",
        description="Persona dueña o responsable de una mascota.",
        id="cliente",
    )

    jefe_rrh = model.add_person(
        location=Location.Internal,
        name="Jefatura de recursos humanos",
        description="La persona de gestiona las cargas horarias de los personal_medicos",
        id="jefeRrh",
    )
    jefe_rrh.tags.add(business_staff_tag)
    #cliente.interacts_with(
    #    jefe_rrh, "Asks questions to", technology="Telephone"
    #)

    personal_medico = model.add_person(
        location=Location.Internal,
        name="personal_medico",
        description="Personal Medico y Personal Tecnico en veterinaria",
        id="personalMedico",
    )
    personal_medico.tags.add(business_staff_tag)

    sistema_gestion_citas_context_container = model.add_software_system(
        location=Location.Internal,
        name="Sistema de Clinica Veterinaria",
        description=(
            "Sistema de Gestion de atencioniones Veterinarias"
        ),
        id="sistemaGestionCitasMedicas",
    )

    cliente.uses(
        sistema_gestion_citas_context_container, "Agenda una cita con su medico pefrerido"
    )
    jefe_rrh.uses(sistema_gestion_citas_context_container, "Registra la carga horario del personal medico")
    personal_medico.uses(sistema_gestion_citas_context_container, "Consulta su carga horaria. Registra el diagnostico y recetas")
    
   
       
    email_system = model.add_software_system(
        location=Location.External,
        name="Gmail",
        description="Gmail",
        id="email",
    )
    email_system.tags.add(existing_system_tag)
    email_system.delivers(
        destination=cliente,
        description="Sends e-mails to",
    )
    sistema_gestion_citas_context_container.uses(
        destination=email_system,
        description="Sends e-mail using",
    )

    whatsapp_system = model.add_software_system(
        location=Location.External,
        name="Whatsapp",
        description="Whatsapp",
        id="whatsappSystem",
    )
    whatsapp_system.tags.add(existing_system_tag)
    whatsapp_system.delivers(
        destination=cliente,
        description="Envia mensajes de texto",
    )
    sistema_gestion_citas_context_container.uses(
        destination=whatsapp_system,
        description="Envia mensajes de texto",
    )
     
    # containers
    portal = sistema_gestion_citas_context_container.add_container(
        name="Portal Institucional",
        description="Web Estatica con informacion de la Organizacion.",
        technology = "Flutter",
        id="portal",
    )
    portal.tags.add(web_browser_tag)
    cliente.uses(portal, "")
    sistema_gestion_citas_context_container.uses(portal, "Publica Promociones")

    single_page_application = sistema_gestion_citas_context_container.add_container(
        "Single-Page Application",
        "Provee la funcionalidad para reservar cita medica, visualizar historial medico.",
        "Flutter",
        id="singlePageApplication",
    )
    single_page_application.tags.add(web_browser_tag)
    cliente.uses(single_page_application, "Uses", technology="JSON/HTTPS")
    jefe_rrh.uses(single_page_application, "Uses", technology="JSON/HTTPS")
    personal_medico.uses(single_page_application, "Uses", technology="JSON/HTTPS")

    mobile_app = sistema_gestion_citas_context_container.add_container(
        "Mobile App",
        "Provee funcionalidad de avisos y comunicacion hacia los clientes.",
        "Flutter",
        id="mobileApp",
    )
    mobile_app.tags.add(mobile_app_tag)
    cliente.uses(mobile_app, "Uses")

    
    api_application_container = sistema_gestion_citas_context_container.add_container(
        "API Gateway",
        "Provee los EndPoints via a JSON/HTTPS API.",
        "NestJs",
        id="apiApplication",
    )
    api_application_container.uses(email_system, "Sends e-mail using", technology="SMTP")
    api_application_container.uses(whatsapp_system, "Envia mensajes", technology="JSON/HTTPS")
    single_page_application.uses(api_application_container, "Makes API calls to" "JSON/HTTPS")
    mobile_app.uses(api_application_container, "Makes API calls to" "JSON/HTTPS")
    portal.uses(api_application_container, "Makes API calls to" "JSON/HTTPS")

    cliente_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto cliente",
        "Provee las funcionalidades para manejar el agregado cliente",
        "NestJs",
        id="clienteContext",
    )
    cliente_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(cliente_context_container, "")

    paciente_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto Paciente",
        "Provee las funcionalidades para manejar el agregado Paciente",
        "NestJs",
        id="pacienteContext",
    )
    paciente_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(paciente_context_container, "")

    comprobante_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto Comprobante",
        "Provee las funcionalidades para manejar el agregado Comprobante",
        "NestJs",
        id="comprobanteContext",
    )
    comprobante_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(comprobante_context_container, "")

    cargahoraria_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto Carga Horaria",
        "Provee las funcionalidades para manejar el agregado Carga Horaria",
        "NestJs",
        id="cargahorariaContext",
    )
    cargahoraria_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(cargahoraria_context_container, "")

    citas_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto Citas Medicas",
        "Provee las funcionalidades para manejar el agregado Citas a medicas",
        "NestJs",
        id="citasMedicas",
    )
    citas_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(citas_context_container, "")

    cirugias_context_container = sistema_gestion_citas_context_container.add_container(
        "Contexto Cirugia Medicas",
        "Provee las funcionalidades para manejar el agregado Cirugia Medicas",
        "NestJs",
        id="cirugiasMedicas",
    )
    cirugias_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(cirugias_context_container, "")

    database = sistema_gestion_citas_context_container.add_container(
        "Database",
        "Stores user registration information, hashed authentication credentials, "
        "access logs, etc.",
        "Relational Database Schema",
        id="database",
    )
    
    database.tags.add(database_tag)
    cliente_context_container.uses(database, "Guarda los clientes")
    paciente_context_container.uses(database , "Guarda los datos de los pacientes")
    citas_context_container.uses(database, "Guarda los datos de la consulta, diagnistico y prescipcion")
    cirugias_context_container.uses(database, "Guarda los datos de la cirugia")
    comprobante_context_container.uses(database, "Guarda los datos de la cirugia")
    cargahoraria_context_container.uses(database, "Guarda los datos de la cirugia")


    
    
    #web_application.uses(
    #    single_page_application, "Delivers to the clientes web browser"
    #)
    #api_application_container.uses(database, "Reads from and writes to", technology="JDBC")
    #api_application_container.uses(mainframe_business_system, "Uses", technology="XML/HTTPS")
    


    
    # COMPONENTS
    # - for a real-world software system, you would probably want to extract the
    #   components using static analysis/reflection rather than manually specifying
    #   them all

    # api_application_container - COMPONENTS
    signin_controller_component = api_application_container.add_component(
        name="Sign In Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="signinController",
    )
    single_page_application.uses(signin_controller_component, "Makes API calls to", "JSON/HTTPS")
    mobile_app.uses(signin_controller_component, "Makes API calls to", "JSON/HTTPS")

    reset_password_controller_component = api_application_container.add_component(
        name="Reset Password Controller",
        description="Allows users to reset their passwords with a single use URL.",
        technology="NestJs - TypeScript",
        id="resetPasswordController",
    )
    single_page_application.uses(reset_password_controller_component, "Makes API calls to", "JSON/HTTPS")
    mobile_app.uses(reset_password_controller_component, "Makes API calls to", "JSON/HTTPS")

    email_component = api_application_container.add_component(
        name="E-mail Component",
        description="Sends e-mails to users.",
        technology="NestJs - TypeScript",
        id="emailComponent",
    )
    email_component.uses(email_system, "Sends e-mail using", technology="SMTP")
    reset_password_controller_component.uses(email_component, "Uses")

    security_component = api_application_container.add_component(
        name="Security Component",
        description="Provides functionality related to signing in, changing passwords, etc.",
        technology="NestJs - TypeScript, GoogleAuth",
        id="securityComponent",
    )
    security_component.uses(database, "Reads from and writes to", "JDBC")
    signin_controller_component.uses(security_component, "Uses")
    reset_password_controller_component.uses(security_component, "Uses")
    
    #paciente_context_container - COMPONENTS
    convocatoria_controller_component = paciente_context_container.add_component(
        name="Convocatoria Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaControllerComponent",
    )
    api_application_container.uses(convocatoria_controller_component)
    
    convocatoria_service_component = paciente_context_container.add_component(
        name="Convocatoria Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaServiceComponent",
    )
    convocatoria_controller_component.uses(convocatoria_service_component)

    convocatoria_repository_component = paciente_context_container.add_component(
        name="Convocatoria Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaRepository",
    )
    convocatoria_repository_component.uses(database)
    convocatoria_service_component.uses(convocatoria_repository_component)

    convocatoria_query_component = paciente_context_container.add_component(
        name="Convocatoria Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaQuery",
    )
    convocatoria_query_component.uses(database)
    convocatoria_controller_component.uses(convocatoria_query_component)
    
    # cliente_context_container - COMPONENTS
    cliente_controller_component = cliente_context_container.add_component(
        name="cliente Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="clienteControllerComponent",
    )
    api_application_container.uses(cliente_controller_component)
    
    cliente_service_component = cliente_context_container.add_component(
        name="cliente Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="clienteServiceComponent",
    )
    cliente_controller_component.uses(cliente_service_component)

    cliente_repository_component = cliente_context_container.add_component(
        name="cliente Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="clienteRepository",
    )
    cliente_repository_component.uses(database)
    cliente_service_component.uses(cliente_repository_component)

    cliente_query_component = cliente_context_container.add_component(
        name="cliente Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="clienteQuery",
    )
    cliente_query_component.uses(database)
    cliente_controller_component.uses(cliente_query_component)

    # citas_context_container - COMPONENTS
    evaluaciones_controller_component = citas_context_container.add_component(
        name="Evaluaciones Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesControllerComponent",
    )
    api_application_container.uses(evaluaciones_controller_component)
    
    evaluaciones_service_component = citas_context_container.add_component(
        name="Evaluaciones Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesServiceComponent",
    )
    evaluaciones_controller_component.uses(evaluaciones_service_component)

    evaluaciones_repository_component = citas_context_container.add_component(
        name="Evaluaciones Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesRepository",
    )
    evaluaciones_repository_component.uses(database)
    evaluaciones_service_component.uses(evaluaciones_repository_component)

    evaluaciones_query_component = citas_context_container.add_component(
        name="Evaluaciones Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesQuery",
    )
    evaluaciones_query_component.uses(database)
    evaluaciones_controller_component.uses(evaluaciones_query_component)

    """
    # TODO:!
    # model.AddImplicitRelationships()

    # deployment nodes and container instances
    developer_laptop = model.add_deployment_node(
        environment="Development",
        name="Developer Laptop",
        description="A developer laptop.",
        technology="Microsoft Windows 10 or Apple macOS",
    )
    apache_tomcat = developer_laptop.add_deployment_node(
        name="Docker - Web Server",
        description="A Docker container.",
        technology="Docker",
    ).add_deployment_node(
        name="Apache Tomcat",
        description="An open source Java EE web server.",
        technology="Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    )
    apache_tomcat.add_container(web_application)
    apache_tomcat.add_container(api_application_container)

    developer_laptop.add_deployment_node(
        "Docker - Database Server", "A Docker container.", "Docker"
    ).add_deployment_node(
        "Database Server", "A development database.", "Oracle 12c"
    ).add_container(
        database
    )

    developer_laptop.add_deployment_node(
        "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    ).add_container(single_page_application)

    cliente_mobile_device = model.add_deployment_node(
        "Customer's mobile device", "", "Apple iOS or Android", environment="Live"
    )
    cliente_mobile_device.add_container(mobile_app)

    cliente_computer = model.add_deployment_node(
        "Customer's computer",
        "",
        "Microsoft Windows or Apple macOS",
        environment="Live",
    )
    cliente_computer.add_deployment_node(
        "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    ).add_container(single_page_application)

    big_bank_data_center = model.add_deployment_node(
        "Big Bank plc", "", "Big Bank plc data center", environment="Live"
    )

    live_web_server = big_bank_data_center.add_deployment_node(
        "bigbank-web***",
        "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
        "Ubuntu 16.04 LTS",
        instances=4,
        properties={"Location": "London and Reading"},
    )
    live_web_server.add_deployment_node(
        "Apache Tomcat",
        "An open source Java EE web server.",
        "Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    ).add_container(web_application)

    live_api_server = big_bank_data_center.add_deployment_node(
        "bigbank-api***",
        "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
        "Ubuntu 16.04 LTS",
        instances=8,
        properties={"Location": "London and Reading"},
    )
    live_api_server.add_deployment_node(
        "Apache Tomcat",
        "An open source Java EE web server.",
        "Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    ).add_container(api_application_container)

    primary_database_server = big_bank_data_center.add_deployment_node(
        "bigbank-db01",
        "The primary database server.",
        "Ubuntu 16.04 LTS",
        instances=1,
        properties={"Location": "London"},
    ).add_deployment_node(
        "Oracle - Primary", "The primary, live database server.", "Oracle 12c"
    )
    primary_database_server.add_container(database)

    big_bank_db_02 = big_bank_data_center.add_deployment_node(
        "bigbank-db02",
        "The secondary database server.",
        "Ubuntu 16.04 LTS",
        instances=1,
        properties={"Location": "Reading"},
    )
    big_bank_db_02.tags.add(failover_tag)
    secondary_database_server = big_bank_db_02.add_deployment_node(
        "Oracle - Secondary",
        "A secondary, standby database server, used for failover purposes only.",
        "Oracle 12c",
    )
    secondary_database_server.tags.add(failover_tag)
    secondary_database = secondary_database_server.add_container(database)

    # model.Relationships.Where(r=>r.Destination.Equals(secondary_database)).ToList()
    #   .ForEach(r=>r.tags.add(failover_tag))
    data_replication_relationship = primary_database_server.uses(
        secondary_database_server, "Replicates data to"
    )
    secondary_database.tags.add(failover_tag)
    """
    # views/diagrams
    system_landscape_view = views.create_system_landscape_view(
        key="SystemLandscape",
        description="Vision global del nuevo Sistema de Clinica Veterinaria",
    )
    system_landscape_view.add_all_elements()
    system_landscape_view.paper_size = PaperSize.A4_Landscape
    
    system_context_view = views.create_system_context_view(
        software_system=sistema_gestion_citas_context_container,
        key="SystemContext",
        description="Diagrama de Contexto del nuevo Sistema de Clinica Veterinaria.",
    )
    system_context_view.enterprise_boundary_visible = True
    #system_context_view.add_all_elements()
    system_context_view.add_nearest_neighbours(sistema_gestion_citas_context_container)
    system_context_view.paper_size = PaperSize.A4_Landscape
    
    container_view = views.create_container_view(
        software_system=sistema_gestion_citas_context_container,
        key="Containers",
        description="Diagrama de contenedores.",
    )
    container_view.add(cliente)
    container_view.add(jefe_rrh)
    container_view.add(personal_medico)
    container_view.add_all_containers()
    container_view.add(email_system)
    container_view.add(whatsapp_system)
    container_view.paper_size = PaperSize.A3_Landscape
    
    # component_apiApplication_view = views.create_component_view(
    #     container=api_application_container,
    #     key="Components",
    #     description="The component diagram for the API Application.",
    # )
    # component_apiApplication_view.add(mobile_app)
    # component_apiApplication_view.add(single_page_application)
    # component_apiApplication_view.add(database)
    # component_apiApplication_view.add_all_components()
    # component_apiApplication_view.add(email_system)
    # component_apiApplication_view.paper_size = PaperSize.A4_Landscape

    # component_convocatoriaContext_view = views.create_component_view(
    #     container=paciente_context_container,
    #     key="Components1",
    #     description="Diagrama de componentes del Bounded Context de Convocatoria.",
    # )
    # component_convocatoriaContext_view.add(api_application_container)
    # component_convocatoriaContext_view.add(database)
    # component_convocatoriaContext_view.add_all_components()
    # component_convocatoriaContext_view.paper_size = PaperSize.A4_Landscape

    # component_clienteContext_view = views.create_component_view(
    #     container=cliente_context_container,
    #     key="Components2",
    #     description="Diagrama de componentes del Bounded Context de clientes.",
    # )
    # component_clienteContext_view.add(api_application_container)
    # component_clienteContext_view.add(database)
    # component_clienteContext_view.add_all_components()
    # component_clienteContext_view.paper_size = PaperSize.A4_Landscape

    # component_evaluacionesContext_view = views.create_component_view(
    #     container=citas_context_container,
    #     key="Components3",
    #     description="Diagrama de componentes del Bounded Context de Evaluaciones.",
    # )
    # component_evaluacionesContext_view.add(api_application_container)
    # component_evaluacionesContext_view.add(database)
    # component_evaluacionesContext_view.add_all_components()
    # component_evaluacionesContext_view.paper_size = PaperSize.A4_Landscape


    """
    # systemLandscapeView.AddAnimation(sistema_gestion_citas_context_container, cliente,
    #   mainframe_business_system, emailSystem)
    # systemLandscapeView.AddAnimation(portal)
    # systemLandscapeView.AddAnimation(clienteServiceStaff, personal_medico)

    # systemContextView.AddAnimation(sistema_gestion_citas_context_container)
    # systemContextView.AddAnimation(cliente)
    # systemContextView.AddAnimation(mainframe_business_system)
    # systemContextView.AddAnimation(emailSystem)

    # containerView.AddAnimation(cliente, mainframe_business_system, emailSystem)
    # containerView.AddAnimation(webApplication)
    # containerView.AddAnimation(singlePageApplication)
    # containerView.AddAnimation(mobile_app)
    # containerView.AddAnimation(apiApplication)
    # containerView.AddAnimation(database)

    # componentView.AddAnimation(singlePageApplication, mobile_app)
    # componentView.AddAnimation(signinController, securityComponent, database)
    # componentView.AddAnimation(accountsSummaryController,
    #   mainframe_business_systemFacade, mainframe_business_system)
    # componentView.AddAnimation(resetPasswordController, emailComponent, database)

    dynamic_view = views.create_dynamic_view(
        element=api_application_container,
        key="SignIn",
        description="Summarises how the sign in feature works in the single-page application.",
    )
    dynamic_view.add(
        single_page_application, signin_controller_component, "Submits credentials to"
    )
    dynamic_view.add(
        signin_controller_component, security_component, "Calls isAuthenticated() on"
    )
    dynamic_view.add(
        security_component, database, "select * from users where username = ?"
    )
    dynamic_view.paper_size = PaperSize.A5_Landscape

    development_deployment_view = views.create_deployment_view(
        software_system=sistema_gestion_citas_context_container,
        key="DevelopmentDeployment",
        description="An example development deployment scenario for the Internet "
        "Banking System.",
        environment="Development",
    )
    development_deployment_view.add(developer_laptop)
    development_deployment_view.paper_size = PaperSize.A5_Landscape

    live_deployment_view = views.create_deployment_view(
        software_system=sistema_gestion_citas_context_container,
        key="LiveDeployment",
        description="An example live deployment scenario for the Internet Banking "
        "System.",
        environment="Live",
    )
    live_deployment_view += big_bank_data_center
    live_deployment_view += cliente_mobile_device
    live_deployment_view += cliente_computer
    live_deployment_view += data_replication_relationship
    live_deployment_view.paper_size = PaperSize.A5_Landscape
    """
    # colours, shapes and other diagram styling
    styles = views.configuration.styles
    styles.add(ElementStyle(tag=Tags.SOFTWARE_SYSTEM, background="#1168bd", color="#ffffff"))
    styles.add(ElementStyle(tag=Tags.CONTAINER, background="#438dd5", color="#ffffff"))
    styles.add(ElementStyle(tag=Tags.COMPONENT, background="#85bbf0", color="#000000"))
    styles.add(ElementStyle(tag=Tags.PERSON, background="#08427b", color="#ffffff", shape=Shape.Person, font_size=22,))
    styles.add(ElementStyle(tag=existing_system_tag, background="#999999", color="#ffffff"))
    styles.add(ElementStyle(tag=business_staff_tag, background="#999999", color="#ffffff"))
    styles.add(ElementStyle(tag=web_browser_tag, shape=Shape.WebBrowser))
    styles.add(ElementStyle(tag=mobile_app_tag, shape=Shape.MobileDeviceLandscape))
    styles.add(ElementStyle(tag=database_tag, shape=Shape.Cylinder))
    styles.add(ElementStyle(tag=failover_tag, opacity=25))
    styles.add(ElementStyle(tag=bounded_context_tag, shape=Shape.Hexagon,background="#facc2e"))
    styles.add(RelationshipStyle(tag=failover_tag, opacity=25, position=70))
    
    

    return workspace

from structurizr import StructurizrClient, StructurizrClientSettings

if __name__ == "__main__":
    #logging.basicConfig(level="INFO")
    workspace = main()
    settings = StructurizrClientSettings(
        workspace_id=70818,
        api_key='ca5604a1-4407-42f6-9dab-9384b65c8152',
        api_secret='aef76fda-e72c-49c4-838c-f42dd6f48379',
    )
    client = StructurizrClient(settings=settings)
    
    workspace.id = client.get_workspace().id
    client.put_workspace(workspace)
