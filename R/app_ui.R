#' The application User-Interface
#'
#' @param request Internal parameter for `{shiny}`.
#'     DO NOT REMOVE.
#' @import shiny bs4Dash
#' @noRd
app_ui <- function(request) {
  tagList(
    # Leave this function for adding external resources
    golem_add_external_resources(),
    # Your application UI logic
    dashboardPage(
      
      dashboardHeader(title = "Kwowledge Impact"),
      
      dashboardSidebar(
        sidebarMenu(
          menuItem("Home", tabName = "home", icon = icon("home")),
          menuItem("My Profile", tabName = "profile", icon = icon("user")),
          menuItem("Analytics", tabName = "analytics", icon = icon("th")),
          menuItem("My Research", tabName = "research", icon = icon("search")),
          menuItem("Calendar", tabName = "calendar", icon = icon("calendar")),
          menuItem("Notifications", tabName = "notifications", icon = icon("th")),
          menuItem("Help Center", tabName = "help", icon = icon("bell")),
          menuItem("Settings", tabName = "settings", icon = icon("cog"))
        )
      ),
      
      dashboardBody(
        tabItems(
          
          # Home
          tabItem(tabName = "home"),
          
          # Profile
          tabItem(tabName = "profile"),
          
          # Analytics
          tabItem(tabName = "analytics"),
          
          # Research
          tabItem(tabName = "research"),
          
          # Calendar
          tabItem(tabName = "calendar"),
          
          # Notifications
          tabItem(tabName = "notifications"),
          
          # Help
          tabItem(tabName = "help"),
          
          # Settings
          tabItem(tabName = "settings")
          
        )
      )
    )
  )
}

#' Add external Resources to the Application
#'
#' This function is internally used to add external
#' resources inside the Shiny application.
#'
#' @import shiny
#' @importFrom golem add_resource_path activate_js favicon bundle_resources
#' @noRd
golem_add_external_resources <- function() {
  add_resource_path(
    "www",
    app_sys("app/www")
  )

  tags$head(
    favicon(),
    bundle_resources(
      path = app_sys("app/www"),
      app_title = "projectimpact"
    )
    # Add here other external resources
    # for example, you can add shinyalert::useShinyalert()
  )
}
