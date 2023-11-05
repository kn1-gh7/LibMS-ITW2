from django.db import models
from django.forms import ValidationError

# Create your models here.

class Books(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=50, blank=True, null=True)
    year_published = models.IntegerField(null=True, blank=True)
    description_text = models.CharField(max_length=200,null=True, blank=True)

class Users(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True,)
    name = models.CharField(max_length=50, null=False)

class TransactionTypes(models.Model):
    t_type = models.PositiveSmallIntegerField(primary_key=True)
    t_name = models.CharField(max_length=30, null=False)


class Genres(models.Model):
    label = models.IntegerField(primary_key=True)
    categories = models.CharField(max_length=40)


class BookGenres(models.Model):
    book_ISBN = models.ForeignKey(Books, on_delete=models.CASCADE, to_field="ISBN")
    genres = models.ForeignKey(Genres, on_delete=models.CASCADE, to_field= "label")

class LibraryDB(models.Model):
    book_isbn = models.ForeignKey(Books, on_delete=models.CASCADE, primary_key=True)
    total_count = models.IntegerField(null=False, default=0)
    issued_count = models.IntegerField(null=False, default=0)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check= models.Q(total_count__gt=models.F("issued_count")) & models.Q(issued_count__gte=0),
                name="not_more_books_issued",
                violation_error_message="ERROR: Either trying to return a book which was not issued,"
                                                " or trying to issue more books that available!"
            )
        ]
    def clean(self):
        if not (self.total_count >= self.issued_count >= 0):
            raise ValidationError('ERROR: Either trying to return a book which was not issued, or trying to issue more books that available!')
    

class BooksAndUsers(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Transactions(models.Model):
    # trans_ID  = models.AutoField()
    trans_type= models.ForeignKey(TransactionTypes, on_delete=models.CASCADE)
    trans_time = models.DateTimeField()
    the_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    
    # overload save to implement triggers!
    
    def save(self, *args, **kwargs):
        if self.trans_type == 1:
            book = LibraryDB.objects.get_or_create(book_isbn=self.book_id)
            book.issued_count += 1
            book.save()
            
            BooksAndUsers(book_id=self.book_id, user_id=self.the_user_id).save()
            
        elif self.trans_type == 2:
            book = LibraryDB.objects.get_or_create(book_isbn=self.book_id)
            book.issued_count -= 1
            book.save()
            
            BooksAndUsers.objects.filter(book_id=self.book_id, user_id=self.the_user_id).all()[0].delete()
        super(self).save(*args,**kwargs)
