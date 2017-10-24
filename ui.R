## ui.R ##
library(shinydashboard)

shinyUI(dashboardPage(
  skin = 'yellow',
  dashboardHeader(
    title = 'SoundCloud'),
  dashboardSidebar(
    sidebarUserPanel('David Kogan', 
                     image = 'http://icons.iconarchive.com/icons/xenatt/minimalism/256/App-SoundCloud-icon.png'),
    sidebarMenu(
      menuItem('Comment Times', tabName = 'comment_times')
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = 'comment_times',
        fluidRow(
          box(
            selectInput(inputId = 'times_genre',
                        label = 'Select Genre:',
                        choice = genres),
            sliderInput("times_range", "Time Range:",
                        min = 0, max = 600,
                        value = c(0,180))
          )
        ),
        fluidRow(
          box(width = 12,
            plotOutput('times_graph')
          )
        ))
    )
  )
))