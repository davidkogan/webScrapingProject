## server.R ##
shinyServer(function(input, output){
  
  output$times_graph = renderPlot({
    soundcloud %>%
      filter(., genre == input$times_genre) %>%
      ggplot(., aes(x=comment_time)) +
      geom_histogram(binwidth = 1, aes(fill=..count..)) +
      coord_cartesian(xlim = input$times_range) + 
      labs(title='Comment Time Frequencies') +
      labs(x='Time', y='Count')
  })
  
  
})