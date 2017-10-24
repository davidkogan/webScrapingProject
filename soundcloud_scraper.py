from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

#Initialize csv file soundcloud.csv
csv_file = open('soundcloudData.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['artist', 'title', 'date', 'duration', 'song_plays', 'song_likes', 'song_reposts',
	'artist_followers', 'artist_tracks', 'comment_time', 'comment_username', 'comment_content'])

driver = webdriver.Chrome()
#URLs for different genres
genres = ['alternativerock', 'ambient', 'classical', 'country',
		'dancehall', 'deephouse', 'disco', 'drumbass',
		'dubstep', 'electronic', 'folksingersongwriter', 'hiphoprap', 
		'house', 'indie', 'jazzblues', 'latin', 'metal', 'pop', 
		'rbsoul', 'reggae', 'rock', 'techno', 'trap', 'triphop']

urls = ['https://soundcloud.com/charts/top?genre=' 
		+ genre + '&country=US' for genre in genres]


for url in urls:
	driver.get(url)
	#Load all 50 top songs for given genre
	n = 1
	while True:
	    if len(driver.find_elements_by_class_name('chartTracks__item')) == 50:
	        break
	    else:
	        driver.execute_script('scroll(0, {}*500)'.format(n))
	        time.sleep(0.2)
	        n += 1

	#Store all song links in list
	links = []
	songs = driver.find_elements_by_class_name('sc-link-dark')
	for link in songs:
	    links.append(link.get_attribute('href'))
	links = links[1:]
	
	#Loop through each song
	rank = 1
	for link in links:
		#Go to next song
		driver.get(link)
		time.sleep(32) #Sleep in case of advertisement
		driver.find_element_by_css_selector('.sc-button-play.playButton.sc-button.m-stretch').click() #Pause the song
		#Load all comments
		while True:
			try:
				driver.find_element_by_css_selector('.paging-eof.sc-border-light-top')
				break
			except:
				try:
					driver.find_element_by_class_name('inlineError').find_element_by_class_name('sc-button').click()
				except:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.5)
		#Get basic information
		artist = driver.find_element_by_css_selector('.soundTitle__username.g-opacity-transition-500.g-type-shrinkwrap-inline.g-type-shrinkwrap-large-secondary.soundTitle__usernameHero.sc-type-medium').text
		title = driver.find_element_by_css_selector('.soundTitle__title.sc-font.g-type-shrinkwrap-inline.g-type-shrinkwrap-large-primary').text
		date = driver.find_element_by_class_name('relativeTime').get_attribute('title')
		song_plays = driver.find_elements_by_class_name('sc-ministats-item')[0].get_attribute('title')
		song_likes = driver.find_elements_by_class_name('sc-ministats-item')[1].get_attribute('title')
		song_reposts = driver.find_elements_by_class_name('sc-ministats-item')[2].get_attribute('title')
		artist_followers = driver.find_element_by_css_selector('.sc-ministats.sc-ministats-small.sc-ministats-followers').text
		artist_tracks = driver.find_element_by_css_selector('.sc-ministats.sc-ministats-small.sc-ministats-sounds').text
		#Get comments information
		comments = driver.find_elements_by_class_name('commentsList__item')
		for comment in comments:
			
			#Put information in dictionary and write row in csv file
			song_dict = {}
			song_dict['rank'] = rank
			song_dict['artist'] = artist
			song_dict['title'] = title
			song_dict['date'] = date
			song_dict['song_plays'] = song_plays
			song_dict['song_likes '] = song_likes
			song_dict['song_reposts'] = song_reposts
			song_dict['artist_followers'] = artist_followers
			song_dict['artist_tracks'] = artist_tracks
			try:
				song_dict['comment_time'] = comment.find_element_by_css_selector('.commentItem__timestampLink.sc-link-light').text
			except:
				song_dict['comment_time'] = ''
			song_dict['comment_username'] = comment.find_element_by_css_selector('.commentItem__usernameLink.sc-link-light').text
			song_dict['comment_content'] = comment.find_element_by_css_selector('.commentItem__body.sc-hyphenate').text
			writer.writerow(song_dict.values())
		rank += 1
driver.close()
