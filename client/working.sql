CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public ;
CREATE OR REPLACE FUNCTION public.AddArtist(
    ArtistName TEXT
) RETURNS VOID AS 
$$
BEGIN
    INSERT INTO Artists(ArtistName)
    VALUES (ArtistName);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.AddConcert(
    ArtistID INT,
    HoldingDate DATE, 
    Price INT,
    PriceVIP INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Concerts (ArtistID, HoldingDate, Price, PriceVIP)
    VALUES (ArtistID, HoldingDate, Price, PriceVIP);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.AddListener(
    FirstName TEXT,
    LastName TEXT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Listeners(FirstName, LastName)
    VALUES (FirstName, LastName);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.AddBooking(
    concertID INT,
    isVIP BOOLEAN,
    ListenerID INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Bookings (concertID, isVIP, ListenerID)
    VALUES (concertID, isVIP, ListenerID);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.GetAllArtists()
RETURNS TABLE (
    ID INT,
    ArtistName TEXT,
    TotalRevenue INT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Artists ORDER BY ID;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION public.GetAllConcerts()
RETURNS TABLE (
    ID INT,
    ArtistID INT,
    HoldingDate DATE,
    Price INT,
    PriceVIP INT,
    ListenersNumber INT,
    VIPListenersNumber INT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Concerts ORDER BY ID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.GetAllListeners()
RETURNS TABLE (
    ID INT,
    FirstName TEXT,
    LastName TEXT
) AS $$
BEGIN
    RETURN  QUERY SELECT * FROM Listeners ORDER BY ID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.GetAllBookings()
RETURNS TABLE (
    ID INT,
    ConcertID INT,
    ListenerID INT,
    isVIP BOOLEAN
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Bookings ORDER BY ID;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION ChangeListenersNumber() RETURNS TRIGGER AS 
$$
DECLARE concertID INT;
BEGIN
IF (TG_OP IN ('UPDATE', 'DELETE')) THEN
    IF OLD.isVIP THEN
        UPDATE Concerts SET VIPListenersNumber = VIPListenersNumber - 1 WHERE Concerts.ID = OLD.ConcertID;
    ELSE
        UPDATE Concerts SET ListenersNumber = ListenersNumber - 1 WHERE Concerts.ID = OLD.ConcertID;
    END IF;
END IF;
IF (TG_OP IN ('INSERT', 'UPDATE')) THEN
    IF NEW.isVIP THEN
        UPDATE Concerts SET VIPListenersNumber = VIPListenersNumber + 1 WHERE Concerts.ID = NEW.ConcertID;
    ELSE
        UPDATE Concerts SET ListenersNumber = ListenersNumber + 1 WHERE Concerts.ID = NEW.ConcertID;
    END IF;
END IF;
RETURN NULL; 

END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER ChangeListenersNumberTrigger
AFTER INSERT OR UPDATE OR DELETE ON Bookings
FOR EACH ROW
EXECUTE FUNCTION public.ChangeListenersNumber();

CREATE OR REPLACE FUNCTION CalculateTotalRevenue() RETURNS TRIGGER AS
$$
BEGIN
UPDATE Artists SET TotalRevenue = TotalRevenue - OLD.ListenersNumber * OLD.Price - OLD.VIPListenersNumber * OLD.PriceVIP WHERE ID = OLD.ArtistID;
IF (TG_OP = 'UPDATE') THEN
    UPDATE Artists SET TotalRevenue = TotalRevenue + NEW.ListenersNumber * NEW.Price + NEW.VIPListenersNumber * NEW.PriceVIP WHERE ID = NEW.ArtistID;
END IF;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER CalculateTotalRevenueTrigger
AFTER UPDATE OR DELETE ON Concerts
FOR EACH ROW
EXECUTE FUNCTION public.CalculateTotalRevenue();

CREATE OR REPLACE FUNCTION public.UpdateArtist(UpdatingArtistID INT, NewArtistName TEXT) RETURNS VOID AS
$$
BEGIN
UPDATE Artists SET ArtistName = NewArtistName WHERE ID = UpdatingArtistID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.UpdateListener(UpdatingListenerID INT, NewFirstName TEXT, NewLastName TEXT) RETURNS VOID AS
$$
BEGIN
UPDATE Listeners SET FirstName = NewFirstName, LastName = NewLastName WHERE ID = UpdatingListenerID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.UpdateConcert(UpdatingConcertID INT, NewArtistID INT, NewDate DATE, NewPrice INT, NewPriceVIP INT) RETURNS VOID AS
$$
BEGIN 
UPDATE Concerts SET ArtistID = NewArtistID, HoldingDate = NewDate, Price = NewPrice, PriceVIP = NewPriceVIP WHERE ID = UpdatingConcertID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.UpdateBooking(UpdatingBookingID INT, NewConcertID INT, NewListenerID INT, NewISVIP BOOLEAN) RETURNS VOID AS
$$
BEGIN
UPDATE Bookings SET ConcertID = NewConcertID, ListenerID = NewListenerID, isVIP = NewISVIP WHERE ID = UpdatingBookingID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.DeleteArtistByName(DeletingArtistName TEXT) RETURNS VOID AS
$$
BEGIN
DELETE FROM Artists WHERE ArtistName = DeletingArtistName;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.DeleteListenerByLastName(DeletingLastName TEXT) RETURNS VOID AS
$$
BEGIN
DELETE FROM Listeners WHERE LastName = DeletingLastName;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.DeleteListenerByID(DeletingListenerID INT) RETURNS VOID AS
$$
BEGIN
DELETE FROM Listeners WHERE ID = DeletingListenerID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.DeleteConcert(DeletingConcertID INT) RETURNS VOID AS
$$
BEGIN
DELETE FROM Concerts WHERE ID = DeletingConcertID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.DeleteBooking(DeletingBookingID INT) RETURNS VOID AS
$$
BEGIN
DELETE FROM Bookings WHERE ID = DeletingBookingID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GetArtistByName(SearchingArtistName TEXT)
RETURNS TABLE (
    ID INT,
    ArtistName TEXT,
    TotalRevenue INT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Artists WHERE Artists.ArtistName = SearchingArtistName ORDER BY ID;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION DeleteAllArtists() RETURNS VOID AS
$$
BEGIN
DELETE FROM Artists;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION DeleteAllConcerts() RETURNS VOID AS
$$
BEGIN
DELETE FROM Concerts;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION DeleteAllListeners() RETURNS VOID AS
$$
BEGIN
DELETE FROM Listeners;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION DeleteAllBookings() RETURNS VOID AS
$$
BEGIN
DELETE FROM Bookings;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION DeleteAll() RETURNS VOID  AS
$$
BEGIN
DELETE FROM Artists;
DELETE FROM Listeners;
END;
$$ LANGUAGE plpgsql;