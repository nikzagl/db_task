CREATE OR REPLACE FUNCTION create_all_tables() RETURNS void AS
$$
BEGIN
CREATE TABLE IF NOT EXISTS public.Artists (
    ID SERIAL PRIMARY KEY,
    ArtistName TEXT,
    TotalRevenue INT DEFAULT 0
);
CREATE TABLE IF NOT EXISTS public.Concerts (
    ID SERIAL PRIMARY KEY,
    ArtistID INT NOT NULL,
    HoldingDate DATE,
    Price INT NOT NULL,
    PriceVIP INT NOT NULL,
    ListenersNumber INT DEFAULT 0,
    VIPListenersNumber INT DEFAULT 0,
    FOREIGN KEY (ArtistID) REFERENCES Artists(ID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS public.Listeners (
    ID SERIAL PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT
);
CREATE TABLE IF NOT EXISTS public.Bookings (
    ID SERIAL PRIMARY KEY,
    ConcertID INT NOT NULL,
    ListenerID INT NOT NULL,
    isVIP BOOLEAN,
    FOREIGN KEY (ConcertID) REFERENCES Concerts(ID) ON DELETE CASCADE,
    FOREIGN KEY (ListenerID) REFERENCES Listeners(ID) ON DELETE CASCADE
    );
CREATE INDEX IF NOT EXISTS Artists_idx ON Artists(ArtistName);
CREATE INDEX IF NOT EXISTS Listeners_lastname ON Listeners(LastName);
GRANT SELECT, UPDATE, INSERT, DELETE ON public.Artists to editor;
GRANT SELECT, UPDATE, INSERT, DELETE ON public.Listeners to editor;
GRANT SELECT, UPDATE, INSERT, DELETE ON public.Concerts to editor;
GRANT SELECT, UPDATE, INSERT, DELETE ON public.Bookings to editor;
END;
$$ LANGUAGE plpgsql;


