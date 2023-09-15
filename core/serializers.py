from djoser.serializers import UserCreateSerializer as UserCreate, UserSerializer as BaseUser


class UserCreateSerializer(UserCreate):
    class Meta(UserCreate.Meta):
        fields = ('id', 'email', 'username',
                  'password', 'first_name', 'last_name')


class CurrentUser(BaseUser):
    class Meta(BaseUser.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
