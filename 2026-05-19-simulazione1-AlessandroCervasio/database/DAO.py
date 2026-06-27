from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.*
                    from genre g """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*
                    from artist a 
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistGenre(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with tabella1 as(
                    select a.ArtistId 
                    from track t 
                    join album a on a.AlbumId = t.AlbumId 
                    where t.GenreId = %s
                    )
                    select a.*
                    from artist a 
                    join tabella1 on a.ArtistId = tabella1.artistid"""

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCoppieArtistGenre(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with tabella1 as (
                select i.CustomerId, i2.TrackId 
                from invoice i 
                join invoiceline i2 on i.InvoiceId = i2.InvoiceId 
                ),
                tabella2 as (
                select distinct t.AlbumId, tabella1.customerid 
                from track t 
                join tabella1 on t.TrackId = tabella1.trackid 
                where t.GenreId = %s
                ),
                tabella3 as (
                select distinct a.ArtistId , tabella2.customerid 
                from album a 
                join tabella2 on a.AlbumId = tabella2.albumid 
                )
                select distinct a.artistid as aid, b.artistid as bid
                from tabella3 a, tabella3 b
                where a.artistid < b.artistid 
                and a.customerid = b.customerid"""

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append((row["aid"], row["bid"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolaritaArtistGenre(artistId, genreId):
        conn = DBConnect.get_connection()



        cursor = conn.cursor(dictionary=True)
        query = """with tabella1 as (
                select t.TrackId 
                from album a 
                join track t on t.AlbumId = a.AlbumId
                where a.ArtistId = %s
                and t.GenreId = %s
                )
                select sum(i.Quantity) as popolarita
                from invoiceline i 
                join tabella1 on tabella1.trackid = i.TrackId """

        cursor.execute(query, (artistId, genreId))

        for row in cursor:
            result=row["popolarita"]

        cursor.close()
        conn.close()
        return result



