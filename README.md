# qCalculus

## Background
I built this project shortly after completing the [Udacity CS253](https://www.udacity.com/course/cs253) "Web Development" course when it was first released. I wanted to apply my newfound skill at creating webapp2 apps to good use, and at the time I wanted an online portal for my students to access lessons, collaborate, and solve problems. 

qCalculus was built in the summer of 2012, and occupied essentially of my time. At the time, I had no idea what unittest were, and I didn't even know what version control was - I saved all of my code in a dropbox folder and deployed it to the app engine development server to manually check it things were working. While building this I learned how to use twitter bootstrap and the importance of caching objects to improve performance. 

## Features
### Discussion Board
The discussion board allowed my students to ask questions and answer questions. I modeled it very closely after the discussion board that was available to use at Udacity. 
![dicussion boar](https://trello-attachments.s3.amazonaws.com/52f5434f608c36344c97f6e8/52f546247a8727ec7f3f3489/a7e63dc61947b16066991fbb8d018865/Screen_Shot_2014-02-07_at_2.45.00_PM.png)

### Ribbons
I wanted the platform to have a bit of gamification to it, so I created ribbons in photoshop and awarded them to students as they completed certain tasks. Some ribbons were procedurally awarded, others were manually awarded by me. Students loved the ribbons!

![ribbons](https://trello-attachments.s3.amazonaws.com/52f5434f608c36344c97f6e8/52f546247a8727ec7f3f3489/cc41b43da72c7a992ab75f31778d5073/Screen_Shot_2014-02-07_at_2.45.29_PM.png)

![profile-ribbons](https://trello-attachments.s3.amazonaws.com/52f5434f608c36344c97f6e8/52f546247a8727ec7f3f3489/fc01c881fce25c3a3fe948364f36d94a/Screen_Shot_2014-02-07_at_2.44.00_PM.png)

### Videos and Quiz Checkpoints
I really enjoyed the interface at Udacity, so I tried to copy it here. 

![videos](https://trello-attachments.s3.amazonaws.com/52f5434f608c36344c97f6e8/52f546247a8727ec7f3f3489/5f0bd80520452632169a066163810b90/Screen_Shot_2014-02-07_at_2.44.31_PM.png)

## Lessons Learned
I spent the entire summer putting this app together; it truly was my first large software project. Unfortunately, after about 12 weeks of maintaining this app and writing content for the lessons (each video took me quite some time to produce) I simply ran out of time to keep the lessons going. Students really enjoyed the platform, but it was just too difficult for me to maintain. 

I should have known about test-driven development at this time, which would have saved me a ton of frustration as I was trying to discover bugs. It would have also been nice if I had discovered the high replication datastore (NDB) which automatically caches objects - that would have saved a ton of time!


