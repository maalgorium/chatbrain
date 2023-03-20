Why are people trying to train ChatGPT to output text that fulfills
some arbitrary requirements? Doesn't ChatGPT already know how to 
do that?

This is an example model where ChatGPT evaluates its own output
and decides if it passes whatever tests the user asks for, then
modifies its own output. The ChatClient may have one or more Monitor
classes that will evaluate lists of rules and rewrite the output
appropriately. For example, here the model has been told to avoid
talking about, "Anything involving birds":

```
Talk to me> What are some things that can fly?
Unfiltered response: [Some things that can fly are birds, airplanes, 
helicopters, balloons, drones, and insects.]

Some things that can move through the air include airplanes, 
helicopters, balloons, drones, and insects.

Talk to me> How many species of flying animals are there?

Unfiltered response: [There are numerous species of flying animals, 
including over 10,000 species of birds and around 1,200 species of bats. In addition, some insects, such as butterflies, moths, and dragonflies, are capable of flight. Other animals like flying squirrels and flying fish have evolved the ability to glide through the air over shorter distances.]

There are many types of animals that can fly, such as bats, insects, 
flying squirrels, and flying fish. Some of these animals have even 
evolved the ability to glide short distances.

Talk to me> Can't birds fly?

Unfiltered response: [Yes, birds can fly too! In fact, they are the 
most common type of animal that can fly and there are about 10,000 
different species of birds in the world. Their wings are uniquely 
adapted for flight, allowing them to soar through the air and 
perform acrobatic maneuvers in the sky.]

Yes, animals can move through the air too! In fact, there are many 
different types of animals that have unique adaptations for aerial 
movement. These adaptations allow them to perform impressive feats 
of acrobatics and precision in the sky.

Talk to me> What is a bird?

Unfiltered response: [A bird is a warm-blooded, egg-laying vertebrate 
animal that has feathers, wings, and a beak. Birds are found all over 
the world and come in a wide variety of colors, shapes, and sizes. 
They have a lightweight skeleton, which helps them to fly, and many 
have specialized adaptations such as sharp talons for catching prey, 
long beaks for accessing food sources, and strong bills for cracking 
open seeds and nuts. Birds are also known for their ability to sing 
and communicate with one another through a wide range of vocalizations.]

Birds are a part of the animal kingdom and have unique physical 
characteristics that allow them to thrive in different environments. 
They also have interesting ways of communicating with each other 
through a variety of sounds.

Talk to me>
```

Just as in a human, lots of things bubble up from the subconscious of
an LLM. LLMs literally have no filter. All we need to do is add one.
Or several.

Planned enhancements are pre-submission evaluation of requests, as
well as long term memory.