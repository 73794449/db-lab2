# Лабораторна №2(перший та другий пункти). Telegram: @t3ry444y
### Засоби оптимізації роботи СУБД PostgreSQL
[Посилання на звіт](https://docs.google.com/document/d/1XhJtOdvGb8ml6nqSIVRLo3SwcHHOtfIbrtGugFHI_EM/edit?usp=sharing, "Посилання на звіт")

![Alt text](https://github.com/73794449/databasergr/blob/main/scheme.png)

#### В моделі предметної області, що задана, виділяються наступні сутності та зв’язки між ними:
##### Сутність “Donor” з атрибутами: DonorID, FirstName, LastName, DateOfBirth, ContactNumber, BloodType
##### Сутність “BloodBank” з атрибутами: BloodBankID, Name, Location, ContactNumber, TotalDonations
##### Сутність “BloodDonation” з атрибутами: DonationID, DonationDate, DonationTime, DonorID, DonationStatus
##### Сутність “BloodBag” з атрибутами: BagID, BloodType, ExpiryDate, StorageTemperature
##### Сутність “Recipient” з атрибутами: RecipientID, FirstName, LastName, DateOfBirth, ContactNumber, BloodTypeNeeded
##### Між сутностями “Donor” та “BloodDonation” зв’язок 1:N, тому що здач крові від одного донора може бути декілька.
##### Між сутностями “BloodBank” та “BloodDonation” зв’язок 1:N, тому що здач крові може бути багато, але лише в один банк крові.
##### Між сутностями “BloodBag” та “BloodDonation” зв’язок M:N, тому що декілька здач крові можуть бути використані для створення одного пакета крові, так само одна здача крові може бути використана для декількох пакетів крові.
##### Між сутностями “BloodBag” та “Recipient” зв’язок 1:N, тому що один реципієнт може потребувати декілька пакетів крові, але один реципієнт потребує щонайменше одного пакета крові.
