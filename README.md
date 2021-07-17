## Movie-library API

### Launch application

+ running
        
        docker-compose up

+ initialize database
        
        docker-compose exec api flask db init
        docker-compose exec api flask db migrate
        docker-compose exec api flask db upgrade

### Default data 

+ to load default data into database
        
        docker-compose exec api flask seed_db

### Project documentation

+ API documentation is available at
        
        http://0.0.0.0:5000/apidocs/
