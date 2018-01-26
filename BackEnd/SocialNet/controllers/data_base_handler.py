"""Class that incapsulates work with data base and add layer of abstraction """

from restNet.models import User, Post
from restNet.serializer import UserSerializer, PostSerializer

class DataBaseHandler:
    """ Class that incapsulates work with data base and add layer of abstraction """

    # Aliases that provide access to different data base models
    _ALIASES = {"user": User,
                "post": Post}

    #  Aliases that provide access to different serializers
    _SERIALIZERS = {"user": UserSerializer,
                    "post": PostSerializer}

    def add_entry(self, alias, dict):
        """ Adds entry to a data base table

         Params:
                alias - name of the table
                dict - number of parameters that new entry should be populated with

         """

        new_entry = self._ALIASES[alias](**dict)
        new_entry.save()

    def delete_entry(self, alias, dict):
        """ Deletes entry from a data base table

            Params:
                    alias - name of the table
                    dict - dictionary with attributes by which entries should be filtered

        """

        self._ALIASES[alias].objects.filter(**dict).delete()

    def update_entry(self, alias, upd_dict, search_dict):
        """ Updates entry of a data base table

            Params:
                    alias - name of the table
                    upd_dict - parameters which should be set in db entry
                    search_dict - parameters by which entries for update should be filtered

        """

        entry = self._ALIASES[alias].objects.filter(**search_dict).first()

        for key in upd_dict:
            setattr(entry, key, upd_dict[key])
        entry.save()

    def contains(self, alias, dict):
        """ Function that checks if entry exists in data base table

            Params:
                    alias - name of the table
                    dict - number of parameters that entries are filtered by

            Returns:
                    True - if entry exists
                    False - if entry does not exist
        """

        if self._ALIASES[alias].objects.filter(**dict).first():
            return True
        else:
            return False

    def get_entry(self, alias, dict, asEntry=False):
        """ Gets and returns single entry from data base

            Params:
                    alias - name of the table
                    dict - number of parameters by which entries are filtered by
                    asEntry - specific how user should receive response

            Returns:
                    Dictionary of entries attributes
                    or Entry itself
        """

        entry = self._ALIASES[alias].objects.filter(**dict).first()
        if asEntry:
            return entry
        else:
            return self._SERIALIZERS[alias](entry).data

    def get_entries(self, alias, dict):
        """ Function that returns list of data base entries that are filtered by input dictionary.

            Params:
                    alias - name of the table
                    dict - number of parameters that entries are filtered by

            Returns:
                    List of dictionary of entries attributes - if entry exists
                    None - if entry does not exist

        """
        entries = self._ALIASES[alias].objects.filter(**dict)

        if entries:
            return [self._SERIALIZERS[alias](entry).data for entry in entries]
        else:
            return None